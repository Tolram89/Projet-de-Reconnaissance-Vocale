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
     "responses": ["Je viens de naitre", "Je suis né en 2025", "Mon anniversaire est le 1 avril"]
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
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')  # Une seule fois si ce n'est pas déjà téléchargé

lemmatizer = WordNetLemmatizer()


all_word = [] #liste pour contenir les tokens
paires_entraînement = [] #liste de tuples ([tokens], tag)

#tokeniser notre data et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        text = pattern.lower()
        text = text.replace("-"," ") # pour séparer les mots composé 
        if " j'" in text or " t'" in text or " m'" in text or  " l'" in text or " s'" in text or " d'" in text  :
            text = text.replace("'",' ')
        tokkens = nltk.word_tokenize(text)
        tokkens = [mot for mot in tokkens if mot not in string.punctuation]
        tokkens = [lemmatizer.lemmatize(mot) for mot in tokkens]

        paires_entraînement.append((tokkens, intent["tag"]))# creer des paires d'entrainement
        all_word.extend(tokkens) # creer un vocabulaire

all_word = sorted(set(all_word))#rend une liste d'éléments uniques  et trier   

tags = [intent["tag"] for intent in data["intents"]] # recupere les tag
tags = sorted(set(tags)) # trier et sans doublon meme si normalement il n'y a pas de doublon si la data est bien faite

bag_of_word = [0]*len(all_word) #vecteur de 0 et 1 qui dit si un mot du vocabulaire est utilisé dans la phrase ou non
x_train = []
y_train = []

for paire in paires_entraînement :
    bag_of_word = [0]*len(all_word) #vecteur de 0 et 1 qui dit si un mot du vocabulaire est utilisé dans la phrase ou non
    for token in paire[0]:
        
        if token in all_word:
            i = all_word.index(token)
            bag_of_word[i] = 1
    x_train.append(bag_of_word)
    y_train.append(paire[1]) # met le tag

from tensorflow.keras.utils import to_categorical

for i in range(0, len(y_train)) :# transforme pour rendre ça comprehensible par le modele
    j = tags.index(y_train[i])
    y_train[i]=j

y_train = to_categorical(y_train) #modele one hot encoding pour de meilleur performance

import numpy as np
x_train = np.array(x_train)
y_train = np.array(y_train)

import json
with open("./voc.json", "w") as f:
    json.dump(all_word, f)
with open("./tags.json", "w") as f:
    json.dump(tags, f)
with open("./data.json", "w") as f:
    json.dump(data, f)

    
#Création du réseaux de neurones
from keras import layers, Model, optimizers, regularizers

input_layer = layers.Input(shape=(len(all_word),))

dense_layer1 = layers.Dense(16, activation='relu')(input_layer)

dense_layer2 = layers.Dense(8, activation='relu')(dense_layer1)

ouput_layer = layers.Dense(len(tags), activation='softmax')(dense_layer2)


# Création du réseau de neurones 
# à partir des couches
model = Model(input_layer, ouput_layer)

#on prend l'optimiseur adam, la Fonction de perte : categorical_crossentropy et pour les metrics : accuracy
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.Adam(),
              metrics=['accuracy'])

#entrainement du modèle
model.fit(x=x_train, y=y_train, batch_size=100, epochs=300)

import os

dir = "./model_architecture"
if not os.path.exists(dir):
    os.makedirs(dir)
dir = dir + "/mon_modele.keras"
model.save(dir)