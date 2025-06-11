import tensorflow as tf
import numpy as np
import random
import re

import nltk
import string
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')  # Une seule fois si ce n'est pas déjà téléchargé
from train_chatbot import get_previous_model_version as get_model_version
from word_key_detection import key_word
import unicodedata

version = get_model_version()
dir = "./model_architecture"
path = dir + "/mon_model_v"+ str(version) + ".keras"
model = tf.keras.models.load_model(path)
lemmatizer = WordNetLemmatizer()

import json

with open("./voc.json", "r", encoding="utf-8") as f:
    all_word = json.load(f)
with open("./tags.json", "r", encoding="utf-8") as f:
    tags = json.load(f)
with open("./data.json", "r", encoding="utf-8") as f:
    data = json.load(f)




def clear_text(text):
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
    preds = model.predict(input_array_bag_of_word)
    intent = preds.argmax()# récupère le plus probable
    return intent
#-----------------------------------------------------
def best_response(intent) :
    tag = tags[intent]

    for intent in data["intents"]:
        if intent["tag"] == tag :
            responses = intent["responses"] # recupere les réponses disponibles 
            response = random.choice(responses) # choisi au hasard parmis une des réponses
            
            if re.search(r"{}", response) : # verifie si il y a un place holder 
                place_holder = key_word(tag) 
                if isinstance(place_holder, (tuple, list)):
                    response = response.format(*place_holder)#remplace le place holder par la véritable réponse, selon si le tupple est un strin ou un tupple
                else:
                    response = response.format(place_holder)
                 
            return response
    return "Je n'ai pas compris."
#-----------------------------------------------------
def speak_with_chatbot(text):

    #tokeniser notre phrase et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
    tokkens = clear_text(text)
    #creer le vecteur bag_of_word et le transforme en tableau numpy
    input_array_bag_of_word = create_input_array(tokkens)

    intent = intention_predict(input_array_bag_of_word)
    response = best_response(intent)
    
    print(response)
    return response
