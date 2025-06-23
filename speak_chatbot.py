import numpy as np
import unicodedata
import string
import random
import re
from word_key_detection import key_word

model = None
lemmatizer = None
all_word = None
tags = None
data = None

def load_chatbot_model(update_progress=None):
    global model, lemmatizer, all_word, tags, data
    if update_progress: update_progress("Chargement de TensorFlow...")
    from tensorflow.keras.models import load_model
    import tensorflow.keras.utils
    if update_progress: update_progress("Chargement de nltk...")
    import nltk
    from nltk.stem import WordNetLemmatizer
    if update_progress: update_progress("Vérification de WordNet...")
    try: 
        nltk.data.find('corpora/wordnet')
    except:
        nltk.download('wordnet')
    if update_progress: update_progress("Chargement du modèle IA...")
    from train_chatbot import get_previous_model_version as get_model_version
    

    version = get_model_version()
    dir = "./model_architecture"
    path = dir + "/mon_model_v"+ str(version) + ".keras"
    model = load_model(path)# charge le model à partir de son chemin
    if update_progress: update_progress("Chargement des fichiers de données...")
    lemmatizer = WordNetLemmatizer()

    import json

    with open("./voc.json", "r", encoding="utf-8") as f:
        all_word = json.load(f)
    with open("./tags.json", "r", encoding="utf-8") as f:
        tags = json.load(f)
    with open("./data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if update_progress: update_progress("Chatbot prêt !")

#-----------------------------------------------------
def clear_text(text):
    import nltk
    global lemmatizer
    text = text.lower()# met tout en minuscule
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )  # retire les accents
    text = text.replace("-"," ") # pour séparer les mots composé 
    text = text.replace("'",' ')
    tokkens = nltk.word_tokenize(text) # je transforme en tokkens
    tokkens = [mot for mot in tokkens if mot not in string.punctuation] #on enlève la ponctuation
    tokkens = [lemmatizer.lemmatize(mot) for mot in tokkens] #et on récupère la racine des mots
    return tokkens
#-----------------------------------------------------
def create_input_array(tokkens):
    global all_word
    word2idx = {mot: i for i, mot in enumerate(all_word)}
    temp_list = []
    for tokken in tokkens:  # Correction ici
        if tokken in all_word:
            i = word2idx[tokken]
            temp_list.append(i)
    # On pad la séquence pour avoir la même taille que lors de l'entraînement (20)
    from tensorflow.keras.utils import pad_sequences
    temp_list = pad_sequences([temp_list], maxlen=20)# normalise la taille du vecteur
    input_array = np.array(temp_list)
    return input_array
#-----------------------------------------------------
def intention_predict(input_array_bag_of_word) :
    global model
    preds = model.predict(input_array_bag_of_word)
    intent = preds.argmax()# récupère le plus probable
    return intent
#-----------------------------------------------------
def best_response(intent, phrase_utilisateur) :
    global tags, data
    tag = tags[intent]

    for intent in data["intents"]:
        if intent["tag"] == tag :
            responses = intent["responses"] # recupere les réponses disponibles 
            response = random.choice(responses) # choisi au hasard parmis une des réponses
            langue_cible="fr" #evite les bugs
            if re.search(r"{}", response) : # verifie si il y a un place holder 

                place_holder, langue_cible  = key_word(tag, phrase_utilisateur) # gère les différentes fonctionnalitées
                if place_holder==None:#pour gérer quand on a un problème avec la météo
                    return None
                else:
                    if isinstance(place_holder, (tuple, list)):
                        response = response.format(*place_holder)#remplace le place holder par la véritable réponse, selon si le tupple est un strin ou un tupple
                    else:
                        response = response.format(place_holder)
                 
            return response, langue_cible
    return "Je n'ai pas compris."
#-----------------------------------------------------
def speak_with_chatbot(text):
    global model
    if model is None:
        load_chatbot_model()  # Chargement sans barre si  pas déjà fait
    langue_cible = "fr"  # Langue par défaut
    #tokeniser notre phrase et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
    tokkens = clear_text(text)

    phrase_utilisateur = text #afin de la transmettre aux fonctionnalité qui en ont besoin
    #creer le vecteur bag_of_word et le transforme en tableau numpy
    input_array_bag_of_word = create_input_array(tokkens)

    intent = intention_predict(input_array_bag_of_word)

    response, langue_cible = best_response(intent, phrase_utilisateur)
    
    print(response)
    return response, langue_cible

#pour le test
"""while True:
    text = input("toi :")
    speak_with_chatbot(text)"""

