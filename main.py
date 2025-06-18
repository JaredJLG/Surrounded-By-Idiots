import os
import openai
import json
from scipy.stats import norm
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
from markupsafe import Markup

# --- Import Project-Specific Modules ---
# These contain the quiz content, normative data for scoring, and AI prompts.
from quiz_content_ipip120 import IPIP_120_QUESTIONS
from normative_data import FACET_NORMS, TRAIT_NORMS
from ai_prompts import get_system_prompt, get_color_prompt, get_romance_prompt, get_work_prompt

# --- APP SETUP ---
app = Flask(__name__)

# --- PRODUCTION-READY CONFIGURATION ---
# This section loads all configuration from environment variables.
# On Replit, these are set using the "Secrets" tool.
# This makes the app secure and portable for deployment.

# 1. Secret Key: Used for session signing. Must be a persistent, secret string.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("FATAL_ERROR: SECRET_KEY not found. Please set it in the Replit Secrets panel.")

# 2. Database URI: Connects to the database. Uses PostgreSQL in production.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise ValueError("FATAL_ERROR: DATABASE_URL not found. Please set it in the Replit Secrets panel.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. OpenAI API Key: For generating AI analyses.
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
if app.config['OPENAI_API_KEY']:
    openai.api_key = app.config['OPENAI_API_KEY']
else:
    print("WARNING: OPENAI_API_KEY secret not found. AI analysis will fail.")
    openai.api_key = None
# --- END CONFIGURATION ---


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- UTILITY FUNCTIONS & FILTERS ---
@app.after_request
def session_cleanup(response):
    # Ensures database connections are properly closed after each request.
    db.session.remove()
    return response

@app.template_filter('markdown')
def markdown_filter(s):
    # Custom template filter to render Markdown in HTML.
    if s is None: return ""
    return Markup(markdown(s, extensions=['fenced_code', 'tables']))

# --- DATABASE MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    results = db.relationship('QuizResult', backref='user', lazy=True)

    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    agreeableness = db.Column(db.Integer, nullable=False)
    conscientiousness = db.Column(db.Integer, nullable=False)
    extraversion = db.Column(db.Integer, nullable=False)
    neuroticism = db.Column(db.Integer, nullable=False)
    openness = db.Column(db.Integer, nullable=False)
    facet_scores_json = db.Column(db.Text, nullable=True)
    ai_feedback = db.Column(db.Text, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- CORE APPLICATION ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    past_results = QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.timestamp.desc()).all()
    return render_template('profile.html', user=current_user, results=past_results)

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html', questions=IPIP_120_QUESTIONS)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    facet_scores_raw = {facet: 0 for facet in FACET_NORMS.keys()}
    trait_scores_raw = {trait: 0 for trait in TRAIT_NORMS.keys()}

    for q in IPIP_120_QUESTIONS:
        answer = request.form.get(f'q_{q["id"]}')
        if not answer:
            flash(f"Question {q['id']} was not answered. Please complete the entire quiz.", 'error')
            return redirect(url_for('quiz'))
        value = int(answer)
        score = (6 - value) if q['direction'] == -1 else value
        facet_scores_raw[q['facet']] += score
        trait_scores_raw[q['trait']] += score

    facet_percentiles = {
        facet: int(round(norm.cdf(raw_score, loc=mean, scale=sd) * 100))
        for facet, raw_score in facet_scores_raw.items()
        for f, (mean, sd) in FACET_NORMS.items() if f == facet
    }
    trait_percentiles = {
        trait: int(round(norm.cdf(raw_score, loc=mean, scale=sd) * 100))
        for trait, raw_score in trait_scores_raw.items()
        for t, (mean, sd) in TRAIT_NORMS.items() if t == trait
    }

    new_result = QuizResult(
        user_id=current_user.id,
        agreeableness=trait_percentiles['agreeableness'],
        conscientiousness=trait_percentiles['conscientiousness'],
        extraversion=trait_percentiles['extraversion'],
        neuroticism=trait_percentiles['neuroticism'],
        openness=trait_percentiles['openness'],
        facet_scores_json=json.dumps(facet_percentiles),
        ai_feedback=None
    )
    db.session.add(new_result)
    db.session.commit()

    return redirect(url_for('analyzing_results', result_id=new_result.id))

# --- AI & RESULTS ROUTES ---

def format_ai_message(trait_scores, facet_scores):
    """Formats the personality scores into a string for the AI prompt."""
    message = "Analyze the following personality profile.\n\n"
    message += "--- OVERALL TRAIT SCORES (Percentiles) ---\n"
    for trait, score in trait_scores.items():
        message += f"- {trait.replace('_', ' ').title()}: {score}%\n"
    message += "\n--- FACET SCORES (Percentiles) ---\n"
    for facet, score in facet_scores.items():
        message += f"- {facet.replace('_', ' ').title()}: {score}%\n"
    return message

def get_ai_feedback(trait_scores, facet_scores):
    """Handles the initial AI analysis call."""
    if not openai.api_key:
        return "### 🚨 Configuration Error\n\nThe OpenAI API key is missing. The administrator needs to set the `OPENAI_API_KEY` in the Replit Secrets panel."

    system_prompt = get_system_prompt()
    user_message = format_ai_message(trait_scores, facet_scores)

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return f"### 😢 AI Analysis Failed\n\nThere was a problem communicating with the AI model.\n\n**Error Details:** `{e}`"

@app.route('/analyzing/<int:result_id>')
@login_required
def analyzing_results(result_id):
    result = db.session.get(QuizResult, result_id)
    if not result or result.user_id != current_user.id:
        flash('You do not have permission to view this result.', 'error')
        return redirect(url_for('profile'))
    return render_template('analyzing.html', result_id=result_id)

@app.route('/get_ai_analysis/<int:result_id>')
@login_required
def get_ai_analysis(result_id):
    """Background route called by the 'analyzing' page to trigger and save the main report."""
    result = db.session.get(QuizResult, result_id)
    if not result or result.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Permission denied'}), 403
    if result.ai_feedback:
        return jsonify({'status': 'complete'})

    trait_scores = {
        'agreeableness': result.agreeableness, 'conscientiousness': result.conscientiousness,
        'extraversion': result.extraversion, 'neuroticism': result.neuroticism, 'openness': result.openness
    }
    facet_scores = json.loads(result.facet_scores_json)
    feedback = get_ai_feedback(trait_scores, facet_scores)

    result.ai_feedback = feedback
    db.session.commit()

    return jsonify({'status': 'complete'})

@app.route('/results/<int:result_id>')
@login_required
def results(result_id):
    result = db.session.get(QuizResult, result_id)
    if not result or result.user_id != current_user.id:
        flash('You do not have permission to view this result.', 'error')
        return redirect(url_for('profile'))
    if not result.ai_feedback:
        return redirect(url_for('analyzing_results', result_id=result.id))
    return render_template('results.html', result=result)

@app.route('/get_extra_analysis/<int:result_id>/<analysis_type>', methods=['GET'])
@login_required
def get_extra_analysis(result_id, analysis_type):
    """API endpoint for the interactive "deep dive" analyses on the results page."""
    result = db.session.get(QuizResult, result_id)
    if not result or result.user_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403

    trait_scores = {
        'agreeableness': result.agreeableness, 'conscientiousness': result.conscientiousness,
        'extraversion': result.extraversion, 'neuroticism': result.neuroticism, 'openness': result.openness
    }
    facet_scores = json.loads(result.facet_scores_json)

    prompts = {
        "color": get_color_prompt(),
        "romance": get_romance_prompt(),
        "work": get_work_prompt()
    }
    system_prompt = prompts.get(analysis_type)
    if not system_prompt:
        return jsonify({'error': 'Invalid analysis type'}), 400

    user_message = format_ai_message(trait_scores, facet_scores)

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
            temperature=0.7,
        )
        feedback = completion.choices[0].message.content
        return jsonify({'feedback': feedback})
    except Exception as e:
        print(f"OpenAI API call for '{analysis_type}' failed: {e}")
        return jsonify({'error': f'AI analysis failed: {e}'}), 500

# --- APP EXECUTION ---
if __name__ == '__main__':
    # This block is ONLY for local development.
    # In production, a Gunicorn server will run the 'app' object directly.
    with app.app_context():
        # This command creates the database tables if they don't exist.
        db.create_all()
    app.run(host='0.0.0.0', port=81)