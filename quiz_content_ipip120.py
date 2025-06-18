# This is a sample of the IPIP-120 questions. A full implementation would have all 120.
# The structure matches what main.py expects.
# direction: 1 means a higher score (e.g., 5 for 'Strongly Agree') increases the trait score.
# direction: -1 means a higher score *decreases* the trait score (reverse-keyed).

IPIP_120_QUESTIONS = [
    # Extraversion
    {'id': 1, 'text': 'Am the life of the party.', 'trait': 'extraversion', 'facet': 'e_gregariousness', 'direction': 1},
    {'id': 2, 'text': 'Don\'t talk a lot.', 'trait': 'extraversion', 'facet': 'e_gregariousness', 'direction': -1},
    {'id': 3, 'text': 'Feel comfortable around people.', 'trait': 'extraversion', 'facet': 'e_warmth', 'direction': 1},
    {'id': 4, 'text': 'Keep in the background.', 'trait': 'extraversion', 'facet': 'e_assertiveness', 'direction': -1},
    # Agreeableness
    {'id': 5, 'text': 'Sympathize with others\' feelings.', 'trait': 'agreeableness', 'facet': 'a_altruism', 'direction': 1},
    {'id': 6, 'text': 'Am not interested in other people\'s problems.', 'trait': 'agreeableness', 'facet': 'a_altruism', 'direction': -1},
    {'id': 7, 'text': 'Feel others\' emotions.', 'trait': 'agreeableness', 'facet': 'a_sympathy', 'direction': 1},
    {'id': 8, 'text': 'Am not really interested in others.', 'trait': 'agreeableness', 'facet': 'a_sympathy', 'direction': -1},
    # Conscientiousness
    {'id': 9, 'text': 'Am always prepared.', 'trait': 'conscientiousness', 'facet': 'c_self_discipline', 'direction': 1},
    {'id': 10, 'text': 'Leave my belongings around.', 'trait': 'conscientiousness', 'facet': 'c_orderliness', 'direction': -1},
    {'id': 11, 'text': 'Pay attention to details.', 'trait': 'conscientiousness', 'facet': 'c_dutifulness', 'direction': 1},
    {'id': 12, 'text': 'Make a mess of things.', 'trait': 'conscientiousness', 'facet': 'c_orderliness', 'direction': -1},
    # Neuroticism
    {'id': 13, 'text': 'Get stressed out easily.', 'trait': 'neuroticism', 'facet': 'n_anxiety', 'direction': 1},
    {'id': 14, 'text': 'Am relaxed most of the time.', 'trait': 'neuroticism', 'facet': 'n_anxiety', 'direction': -1},
    {'id': 15, 'text': 'Worry about things.', 'trait': 'neuroticism', 'facet': 'n_anxiety', 'direction': 1},
    {'id': 16, 'text': 'Seldom feel blue.', 'trait': 'neuroticism', 'facet': 'n_depression', 'direction': -1},
    # Openness
    {'id': 17, 'text': 'Have a rich vocabulary.', 'trait': 'openness', 'facet': 'o_ideas', 'direction': 1},
    {'id': 18, 'text': 'Have difficulty understanding abstract ideas.', 'trait': 'openness', 'facet': 'o_ideas', 'direction': -1},
    {'id': 19, 'text': 'Have a vivid imagination.', 'trait': 'openness', 'facet': 'o_imagination', 'direction': 1},
    {'id': 20, 'text': 'Am not interested in abstract ideas.', 'trait': 'openness', 'facet': 'o_ideas', 'direction': -1},
    # To reach the 50 questions mentioned in the quiz.html template, we add more
    {'id': 21, 'text': 'Start conversations.', 'trait': 'extraversion', 'facet': 'e_assertiveness', 'direction': 1},
    {'id': 22, 'text': 'Have little to say.', 'trait': 'extraversion', 'facet': 'e_gregariousness', 'direction': -1},
    {'id': 23, 'text': 'Insult people.', 'trait': 'agreeableness', 'facet': 'a_modesty', 'direction': -1},
    {'id': 24, 'text': 'Am interested in people.', 'trait': 'agreeableness', 'facet': 'a_sympathy', 'direction': 1},
    {'id': 25, 'text': 'Get chores done right away.', 'trait': 'conscientiousness', 'facet': 'c_self_discipline', 'direction': 1},
    {'id': 26, 'text': 'Often forget to put things back in their proper place.', 'trait': 'conscientiousness', 'facet': 'c_orderliness', 'direction': -1},
    {'id': 27, 'text': 'Have frequent mood swings.', 'trait': 'neuroticism', 'facet': 'n_vulnerability', 'direction': 1},
    {'id': 28, 'text': 'Rarely get irritated.', 'trait': 'neuroticism', 'facet': 'n_anger', 'direction': -1},
    {'id': 29, 'text': 'Am full of ideas.', 'trait': 'openness', 'facet': 'o_ideas', 'direction': 1},
    {'id': 30, 'text': 'Do not have a good imagination.', 'trait': 'openness', 'facet': 'o_imagination', 'direction': -1},
    {'id': 31, 'text': 'Talk to a lot of different people at parties.', 'trait': 'extraversion', 'facet': 'e_gregariousness', 'direction': 1},
    {'id': 32, 'text': 'Like order.', 'trait': 'conscientiousness', 'facet': 'c_orderliness', 'direction': 1},
    {'id': 33, 'text': 'Am quick to anger.', 'trait': 'neuroticism', 'facet': 'n_anger', 'direction': 1},
    {'id': 34, 'text': 'Believe in the importance of art.', 'trait': 'openness', 'facet': 'o_artistic_interests', 'direction': 1},
    {'id': 35, 'text': 'Am easy to satisfy.', 'trait': 'agreeableness', 'facet': 'a_cooperation', 'direction': 1},
    {'id': 36, 'text': 'Often feel blue.', 'trait': 'neuroticism', 'facet': 'n_depression', 'direction': 1},
    {'id': 37, 'text': 'Would describe my experiences as somewhat dull.', 'trait': 'openness', 'facet': 'o_adventurousness', 'direction': -1},
    {'id': 38, 'text': 'Am exacting in my work.', 'trait': 'conscientiousness', 'facet': 'c_achievement_striving', 'direction': 1},
    {'id': 39, 'text': 'Tend to vote for liberal political candidates.', 'trait': 'openness', 'facet': 'o_liberalism', 'direction': 1},
    {'id': 40, 'text': 'Avoid philosophical discussions.', 'trait': 'openness', 'facet': 'o_ideas', 'direction': -1},
    {'id': 41, 'text': 'Can\'t stand being in a crowd of people.', 'trait': 'extraversion', 'facet': 'e_gregariousness', 'direction': -1},
    {'id': 42, 'text': 'Trust what people say.', 'trait': 'agreeableness', 'facet': 'a_trust', 'direction': 1},
    {'id': 43, 'text': 'Am not easily bothered by things.', 'trait': 'neuroticism', 'facet': 'n_vulnerability', 'direction': -1},
    {'id': 44, 'text': 'Like to do things half-way.', 'trait': 'conscientiousness', 'facet': 'c_achievement_striving', 'direction': -1},
    {'id': 45, 'text': 'Tend to be cynical.', 'trait': 'agreeableness', 'facet': 'a_trust', 'direction': -1},
    {'id': 46, 'text': 'Enjoy wild flights of fantasy.', 'trait': 'openness', 'facet': 'o_imagination', 'direction': 1},
    {'id': 47, 'text': 'Am a very private person.', 'trait': 'extraversion', 'facet': 'e_warmth', 'direction': -1},
    {'id': 48, 'text': 'Believe that I am better than others.', 'trait': 'agreeableness', 'facet': 'a_modesty', 'direction': -1},
    {'id': 49, 'text': 'Am always on the go.', 'trait': 'extraversion', 'facet': 'e_activity_level', 'direction': 1},
    {'id': 50, 'text': 'Get angry easily.', 'trait': 'neuroticism', 'facet': 'n_anger', 'direction': 1}
]
