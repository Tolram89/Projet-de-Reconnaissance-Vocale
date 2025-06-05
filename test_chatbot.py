import tensorflow as tf
import numpy as np
import random


from chatbot import get_previous_model_version as get_model_version

version = get_model_version()
dir = "./model_architecture"
path = dir + "/mon_model_v"+ str(version) + ".keras"
model = tf.keras.models.load_model(path)


import nltk
import string
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')  # Une seule fois si ce n'est pas déjà téléchargé

def clear_text(text):
    text = text.lower()# met tout en minuscule
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
            responses = intent["responses"]
    response = random.choice(responses)
    return response
#-----------------------------------------------------
while 1 :
    text = input("Toi : ")

    lemmatizer = WordNetLemmatizer()

    import json

    with open("./voc.json", "r") as f:
        all_word = json.load(f)
    with open("./tags.json", "r") as f:
        tags = json.load(f)
    with open("./data.json", "r") as f:
        data = json.load(f)

    #tokeniser notre phrase et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
    tokkens = clear_text(text)
    #creer le vecteur bag_of_word et le transforme en tableau numpy
    input_array_bag_of_word = create_input_array(tokkens)

    intent = intention_predict(input_array_bag_of_word)
    response = best_response(intent)
    
    print(response)