import tensorflow as tf
import numpy as np
import random

dir = "./model_architecture/mon_modele.keras"
model = tf.keras.models.load_model(dir)


import nltk
import string
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')  # Une seule fois si ce n'est pas déjà téléchargé

def clear_text(text):


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

    text = text.lower()# met tout en minuscule
    text = text.replace("-"," ") # pour séparer les mots composé 
    if " j'" in text or " t'" in text or " m'" in text or  " l'" in text or " s'" in text or " d'" in text  :
        text = text.replace("'",' ')
    tokkens = nltk.word_tokenize(text) # je transforme en tokkens
    tokkens = [mot for mot in tokkens if mot not in string.punctuation]
    tokkens = [lemmatizer.lemmatize(mot) for mot in tokkens]


    bag_of_word = [0]*len(all_word) #vecteur de 0 et 1 qui dit si un mot du vocabulaire est utilisé dans la phrase ou non
    for token in tokkens:
        
        if token in all_word:
            i = all_word.index(token)
            bag_of_word[i] = 1

    input_array = np.array([bag_of_word])#transformation en tableau numpy
    preds = model.predict(input_array)

    intent = preds.argmax()

    tag = tags[intent]

    for intent in data["intents"]:
        if intent["tag"] == tag :
            responses = intent["responses"]
    response = random.choice(responses)
    print(response)