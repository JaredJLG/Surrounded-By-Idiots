# Placeholder normative data for scoring.
# These are NOT real population norms and are for demonstration purposes only.
# A real implementation would source these from psychometric research papers.
# 'loc' is the mean, 'scale' is the standard deviation.

# Each facet has 4 questions, with scores from 1-5.
# Raw score range per facet: 4 to 20.
# Made-up norms for facets:
FACET_NORMS = {
    # Extraversion Facets
    'e_warmth': (14, 3), 'e_gregariousness': (13, 4), 'e_assertiveness': (12, 3.5),
    'e_activity_level': (15, 3), 'e_excitement_seeking': (16, 4), 'e_positive_emotions': (14, 3.5),
    # Agreeableness Facets
    'a_trust': (15, 3), 'a_modesty': (14, 3.5), 'a_altruism': (16, 2.5),
    'a_cooperation': (15, 3), 'a_sympathy': (17, 3), 'a_straightforwardness': (13, 4),
    # Conscientiousness Facets
    'c_self_efficacy': (15, 3), 'c_orderliness': (14, 4.5), 'c_dutifulness': (16, 3),
    'c_achievement_striving': (17, 3.5), 'c_self_discipline': (13, 4), 'c_cautiousness': (15, 3),
    # Neuroticism Facets
    'n_anxiety': (10, 4), 'n_anger': (9, 3.5), 'n_depression': (8, 3.5),
    'n_self_consciousness': (11, 4), 'n_immoderation': (12, 4), 'n_vulnerability': (10, 4.5),
    # Openness Facets
    'o_imagination': (15, 4), 'o_artistic_interests': (13, 5), 'o_emotionality': (14, 3.5),
    'o_adventurousness': (16, 4), 'o_ideas': (17, 3), 'o_liberalism': (14, 4),
}

# Each trait has 6 facets (24 questions total).
# Raw score range per trait: 24 to 120.
# Made-up norms for traits:
TRAIT_NORMS = {
    'extraversion': (84, 15),
    'agreeableness': (90, 14),
    'conscientiousness': (88, 18),
    'neuroticism': (60, 20),
    'openness': (87, 16),
}
