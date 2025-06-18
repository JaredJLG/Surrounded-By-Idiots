# A sample of 50 questions for a Big Five personality assessment.
# 10 questions for each of the 5 traits.
# 5 are positively keyed (a high score means a high trait score).
# 5 are negatively keyed (a high score means a low trait score).
# 'direction' = 1 for positive, -1 for negative (reverse-scored).

BIG_FIVE_QUESTIONS = [
    # === Extraversion ===
    {'id': 1, 'trait': 'extraversion', 'direction': 1, 'text': 'I am the life of the party.'},
    {'id': 2, 'trait': 'extraversion', 'direction': 1, 'text': 'I feel comfortable around people.'},
    {'id': 3, 'trait': 'extraversion', 'direction': 1, 'text': 'I start conversations.'},
    {'id': 4, 'trait': 'extraversion', 'direction': 1, 'text': 'I talk to a lot of different people at parties.'},
    {'id': 5, 'trait': 'extraversion', 'direction': 1, 'text': "I don't mind being the center of attention."},
    {'id': 6, 'trait': 'extraversion', 'direction': -1, 'text': "I don't talk a lot."},
    {'id': 7, 'trait': 'extraversion', 'direction': -1, 'text': 'I keep in the background.'},
    {'id': 8, 'trait': 'extraversion', 'direction': -1, 'text': 'I have little to say.'},
    {'id': 9, 'trait': 'extraversion', 'direction': -1, 'text': "I don't like to draw attention to myself."},
    {'id': 10, 'trait': 'extraversion', 'direction': -1, 'text': 'I am quiet around strangers.'},

    # === Neuroticism ===
    {'id': 11, 'trait': 'neuroticism', 'direction': 1, 'text': 'I get stressed out easily.'},
    {'id': 12, 'trait': 'neuroticism', 'direction': 1, 'text': 'I worry about things.'},
    {'id': 13, 'trait': 'neuroticism', 'direction': 1, 'text': 'I am easily disturbed.'},
    {'id': 14, 'trait': 'neuroticism', 'direction': 1, 'text': 'I get upset easily.'},
    {'id': 15, 'trait': 'neuroticism', 'direction': 1, 'text': 'I have frequent mood swings.'},
    {'id': 16, 'trait': 'neuroticism', 'direction': -1, 'text': 'I am relaxed most of the time.'},
    {'id': 17, 'trait': 'neuroticism', 'direction': -1, 'text': 'I seldom feel blue.'},
    {'id': 18, 'trait': 'neuroticism', 'direction': -1, 'text': "I don't worry about things that have already happened."},
    {'id': 19, 'trait': 'neuroticism', 'direction': -1, 'text': 'I am emotionally stable.'},
    {'id': 20, 'trait': 'neuroticism', 'direction': -1, 'text': 'I rarely feel anxious or fearful.'},

    # === Agreeableness ===
    {'id': 21, 'trait': 'agreeableness', 'direction': 1, 'text': 'I am interested in people.'},
    {'id': 22, 'trait': 'agreeableness', 'direction': 1, 'text': 'I sympathize with others’ feelings.'},
    {'id': 23, 'trait': 'agreeableness', 'direction': 1, 'text': 'I have a soft heart.'},
    {'id': 24, 'trait': 'agreeableness', 'direction': 1, 'text': 'I take time out for others.'},
    {'id': 25, 'trait': 'agreeableness', 'direction': 1, 'text': "I feel others' emotions."},
    {'id': 26, 'trait': 'agreeableness', 'direction': -1, 'text': "I am not really interested in others."},
    {'id': 27, 'trait': 'agreeableness', 'direction': -1, 'text': "I insult people."},
    {'id': 28, 'trait': 'agreeableness', 'direction': -1, 'text': "I am not interested in other people's problems."},
    {'id': 29, 'trait': 'agreeableness', 'direction': -1, 'text': 'I feel little concern for others.'},
    {'id': 30, 'trait': 'agreeableness', 'direction': -1, 'text': 'I can be sarcastic and biting.'},

    # === Conscientiousness ===
    {'id': 31, 'trait': 'conscientiousness', 'direction': 1, 'text': 'I am always prepared.'},
    {'id': 32, 'trait': 'conscientiousness', 'direction': 1, 'text': 'I pay attention to details.'},
    {'id': 33, 'trait': 'conscientiousness', 'direction': 1, 'text': 'I get chores done right away.'},
    {'id': 34, 'trait': 'conscientiousness', 'direction': 1, 'text': 'I like order.'},
    {'id': 35, 'trait': 'conscientiousness', 'direction': 1, 'text': 'I follow a schedule.'},
    {'id': 36, 'trait': 'conscientiousness', 'direction': -1, 'text': 'I leave my belongings around.'},
    {'id': 37, 'trait': 'conscientiousness', 'direction': -1, 'text': 'I make a mess of things.'},
    {'id': 38, 'trait': 'conscientiousness', 'direction': -1, 'text': 'I often forget to put things back in their proper place.'},
    {'id': 39, 'trait': 'conscientiousness', 'direction': -1, 'text': 'I shirk my duties.'},
    {'id': 40, 'trait': 'conscientiousness', 'direction': -1, 'text': 'I am not very methodical.'},

    # === Openness to Experience ===
    {'id': 41, 'trait': 'openness', 'direction': 1, 'text': 'I have a rich vocabulary.'},
    {'id': 42, 'trait': 'openness', 'direction': 1, 'text': 'I have a vivid imagination.'},
    {'id': 43, 'trait': 'openness', 'direction': 1, 'text': 'I have excellent ideas.'},
    {'id': 44, 'trait': 'openness', 'direction': 1, 'text': 'I am quick to understand things.'},
    {'id': 45, 'trait': 'openness', 'direction': 1, 'text': 'I use difficult words.'},
    {'id': 46, 'trait': 'openness', 'direction': -1, 'text': 'I have difficulty understanding abstract ideas.'},
    {'id': 47, 'trait': 'openness', 'direction': -1, 'text': 'I am not interested in abstract ideas.'},
    {'id': 48, 'trait': 'openness', 'direction': -1, 'text': 'I do not have a good imagination.'},
    {'id': 49, 'trait': 'openness', 'direction': -1, 'text': 'I avoid philosophical discussions.'},
    {'id': 50, 'trait': 'openness', 'direction': -1, 'text': 'I prefer concrete tasks over abstract thinking.'},
]
