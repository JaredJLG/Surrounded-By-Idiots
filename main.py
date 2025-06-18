import os
import openai
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from markdown import markdown
from markupsafe import Markup

from quiz_content_big5 import BIG_FIVE_QUESTIONS
from ai_prompts import get_system_prompt

# --- APP SETUP ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Load OpenAI API key from Replit Secrets
app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
if app.config['OPENAI_API_KEY']:
    openai.api_key = app.config['OPENAI_API_KEY']
else:
    print("WARNING: OPENAI_API_KEY secret not found.")
    openai.api_key = None

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.after_request
def session_cleanup(response):
    db.session.remove()
    return response

@app.template_filter('markdown')
def markdown_filter(s):
    if s is None:
        return ""
    return Markup(markdown(s, extensions=['fenced_code', 'tables']))

# --- DATABASE MODELS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    results = db.relationship('QuizResult', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    agreeableness = db.Column(db.Integer, nullable=False)
    conscientiousness = db.Column(db.Integer, nullable=False)
    extraversion = db.Column(db.Integer, nullable=False)
    neuroticism = db.Column(db.Integer, nullable=False)
    openness = db.Column(db.Integer, nullable=False)
    ai_feedback = db.Column(db.Text, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- ROUTES ---
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
    return render_template('quiz.html', questions=BIG_FIVE_QUESTIONS)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    scores = {'agreeableness': 0, 'conscientiousness': 0, 'extraversion': 0, 'neuroticism': 0, 'openness': 0}
    min_score, max_score = 10, 50

    for q in BIG_FIVE_QUESTIONS:
        q_id, trait, direction = q['id'], q['trait'], q['direction']
        answer = request.form.get(f'q_{q_id}')
        if not answer:
            flash(f"Question {q_id} was not answered. Please complete the entire quiz.", 'error')
            return redirect(url_for('quiz'))
        value = int(answer)
        scores[trait] += (6 - value) if direction == -1 else value

    percentiles = {trait: int(round(((raw - min_score) / (max_score - min_score)) * 100)) for trait, raw in scores.items()}

    new_result = QuizResult(
        user_id=current_user.id,
        agreeableness=percentiles['agreeableness'],
        conscientiousness=percentiles['conscientiousness'],
        extraversion=percentiles['extraversion'],
        neuroticism=percentiles['neuroticism'],
        openness=percentiles['openness'],
        ai_feedback=None
    )
    db.session.add(new_result)
    db.session.commit()

    return redirect(url_for('analyzing_results', result_id=new_result.id))


def get_ai_feedback(scores):
    if not openai.api_key:
        return "### 🚨 Configuration Error\n\nThe OpenAI API key is missing. The administrator needs to set the `OPENAI_API_KEY` in the Replit Secrets panel."

    system_prompt = get_system_prompt()
    user_message = f"Here are my Big Five personality scores in percentiles:\n- Agreeableness: {scores['agreeableness']}%\n- Conscientiousness: {scores['conscientiousness']}%\n- Extraversion: {scores['extraversion']}%\n- Neuroticism: {scores['neuroticism']}%\n- Openness to Experience: {scores['openness']}%"

    try:
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
            temperature=0.7,
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
    result = db.session.get(QuizResult, result_id)
    if not result or result.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Permission denied'}), 403

    if result.ai_feedback:
        return jsonify({'status': 'complete'})

    scores = {
        'agreeableness': result.agreeableness,
        'conscientiousness': result.conscientiousness,
        'extraversion': result.extraversion,
        'neuroticism': result.neuroticism,
        'openness': result.openness
    }

    feedback = get_ai_feedback(scores)
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

# Putting db.create_all() back to ensure the DB is created on first run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=81, threaded=False)
