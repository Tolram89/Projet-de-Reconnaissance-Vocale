# utilisation d'un dictionnaire pour représenter un fichier JSON d'intentions
data = {"intents": [
    {"tag": "greeting",
     "patterns": ["Hello", "La forme?", "yo", "Salut", "ça roule?", "Hey", "Coucou"],
     "responses": ["Salut à toi!", "Hello", "Comment vas-tu?", "Salutations!", "Enchanté"]
    },
    {"tag": "goodbye",
     "patterns": ["bye", "Salut", "see ya", "adios", "cya", "à plus", "à bientôt"],
     "responses": ["C'était sympa de te parler", "À plus tard", "On se reparle très vite!"]
    },
    {"tag": "name",
     "patterns": ["Quel est ton prénom?", "Comment tu t'appelles?", "Qui es-tu?"],
     "responses": ["Je m'appelle Bérou", "Je suis Bérou", "Tu peux m'appeler Bérou"]
    },
    {"tag": "age",
     "patterns": ["Quel âge as-tu?", "C'est quand ton anniversaire?", "Quand es-tu né?"],
     "responses": ["J'ai 25 ans", "Je suis né en 1996", "Mon anniversaire est le 3 juillet"]
    },
    {"tag": "date",
     "patterns": ["Quelle est la date aujourd'hui?", "On est quel jour?", "C'est quoi la date?"],
     "responses": ["Aujourd'hui, nous sommes le {date}", "La date du jour est le {date}"]
    },
    {"tag": "heure",
     "patterns": ["Quelle heure est-il?", "Donne-moi l'heure", "Il est quelle heure?"],
     "responses": ["Il est {heure}", "L'heure actuelle est {heure}"]
    },
    {"tag": "météo",
     "patterns": ["Quel temps fait-il?", "Donne-moi la météo", "Il fait beau?", "Quel temps à Dijon?"],
     "responses": ["La température à Dijon est de {temp}°C", "Il fait actuellement {temp}°C avec un vent de {vent} km/h"]
    },
    {"tag": "remerciement",
     "patterns": ["Merci", "Merci beaucoup", "Merci bien", "Je te remercie"],
     "responses": ["Avec plaisir", "Je t'en prie", "N'hésite pas à me demander autre chose"]
    },
    {"tag": "aide",
     "patterns": ["Que sais-tu faire?", "Aide-moi", "Tu peux m'aider?", "Tu fais quoi?"],
     "responses": ["Je peux te donner la météo, l'heure, la date et discuter avec toi !", "Je suis ton assistant vocal, demande-moi ce que tu veux"]
    }
]}

import nltk
import string


all_word = [] #liste pour contenir les tokens

#tokeniser notre data et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        text = pattern.lower()
        tokkens = nltk.word_tokenize(text)
        tokkens = [mot for mot in tokkens if mot not in string.punctuation]
        all_word.extend(tokkens)
all_word = set(all_word)#rend une liste d'éléments uniques     
print(all_word)
        

