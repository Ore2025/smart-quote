"""Citations locales en français (fallback)"""

FRENCH_QUOTES = [
    {'content': "Le succès n'est pas final, l'échec n'est pas fatal : c'est le courage de continuer qui compte.", 'author': 'Winston Churchill', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "La seule façon de faire du bon travail est d'aimer ce que vous faites.", 'author': 'Steve Jobs', 'tags': ['succès', 'passion'], 'theme': 'succès'},
    {'content': "Croyez que vous pouvez le faire et vous êtes à mi-chemin.", 'author': 'Theodore Roosevelt', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "Le bonheur n'est pas quelque chose de prêt à l'emploi. Il vient de vos propres actions.", 'author': 'Dalaï Lama', 'tags': ['bonheur'], 'theme': 'bonheur'},
    {'content': "Dans un an, vous regretterez de ne pas avoir commencé aujourd'hui.", 'author': 'Karen Lamb', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "La meilleure façon de prédire l'avenir est de le créer.", 'author': 'Peter Drucker', 'tags': ['succès'], 'theme': 'succès'},
    {'content': "Soyez vous-même; tous les autres sont déjà pris.", 'author': 'Oscar Wilde', 'tags': ['sagesse'], 'theme': 'sagesse'},
    {'content': "L'imagination est plus importante que le savoir.", 'author': 'Albert Einstein', 'tags': ['sagesse'], 'theme': 'sagesse'},
    {'content': "Le courage n'est pas l'absence de peur, mais la capacité de la vaincre.", 'author': 'Nelson Mandela', 'tags': ['courage'], 'theme': 'courage'},
    {'content': "La vie est ce qui arrive quand vous êtes occupé à faire d'autres plans.", 'author': 'John Lennon', 'tags': ['sagesse'], 'theme': 'sagesse'},
    {'content': "Vous manquez 100% des coups que vous ne tentez pas.", 'author': 'Wayne Gretzky', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "Ce qui ne nous tue pas nous rend plus fort.", 'author': 'Friedrich Nietzsche', 'tags': ['courage'], 'theme': 'courage'},
    {'content': "Soyez le changement que vous voulez voir dans le monde.", 'author': 'Mahatma Gandhi', 'tags': ['inspiration'], 'theme': 'inspiration'},
    {'content': "La plus grande gloire n'est pas de ne jamais tomber, mais de se relever à chaque chute.", 'author': 'Confucius', 'tags': ['courage'], 'theme': 'courage'},
    {'content': "Il n'y a qu'une façon d'échouer, c'est d'abandonner avant d'avoir réussi.", 'author': 'Olivier Lockert', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "L'avenir appartient à ceux qui croient en la beauté de leurs rêves.", 'author': 'Eleanor Roosevelt', 'tags': ['inspiration'], 'theme': 'inspiration'},
    {'content': "Le meilleur moment pour planter un arbre était il y a 20 ans. Le deuxième meilleur moment est maintenant.", 'author': 'Proverbe chinois', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "Ne comptez pas les jours, faites que les jours comptent.", 'author': 'Muhammad Ali', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "La seule limite à notre réalisation de demain sera nos doutes d'aujourd'hui.", 'author': 'Franklin D. Roosevelt', 'tags': ['motivation'], 'theme': 'motivation'},
    {'content': "Agissez comme s'il était impossible d'échouer.", 'author': 'Winston Churchill', 'tags': ['motivation'], 'theme': 'motivation'}
]

def get_random_quote(theme=None):
    import random
    if theme and theme != 'auto':
        filtered = [q for q in FRENCH_QUOTES if theme.lower() in [t.lower() for t in q.get('tags', [])] or q.get('theme', '').lower() == theme.lower()]
        quote = random.choice(filtered) if filtered else random.choice(FRENCH_QUOTES)
    else:
        quote = random.choice(FRENCH_QUOTES)
    quote['length'] = len(quote['content'])
    quote['id'] = f"local_{hash(quote['content'])}"
    quote['source'] = 'local'
    return quote
