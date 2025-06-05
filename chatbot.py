import os
import fnmatch
#---------------------------------------------------------
def get_previous_model_version(folder_path = "./model_architecture", prefix_model = "/mon_model_v") :
    for file in os.listdir(folder_path):
        if fnmatch.fnmatch(file, "*.keras"):
            file = os.path.basename(file).split('v')[-1] #recupère apres le v
            version = os.path.basename(file).split('.')[0]
            return version
        return
#---------------------------------------------------------
if __name__ == "__main__":
    # utilisation d'un dictionnaire pour représenter un fichier JSON d'intentions

    import nltk
    import string
    from nltk.stem import WordNetLemmatizer
    import json
    #nltk.download('wordnet')  # Une seule fois si ce n'est pas déjà téléchargé
    
    with open("./data.json", "r") as f:
        data = json.load(f)
        
    lemmatizer = WordNetLemmatizer()


    all_word = [] #liste pour contenir les tokens
    paires_entraînement = [] #liste de tuples ([tokens], tag)

    #tokeniser notre data et la rendre plus propre en mettant tout en minuscule et en enlevant la ponctuation
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            text = pattern.lower()
            text = text.replace("-"," ") # pour séparer les mots composé 
            text = text.replace("'",' ')
            tokkens = nltk.word_tokenize(text)
            tokkens = [mot for mot in tokkens if mot not in string.punctuation]
            tokkens = [lemmatizer.lemmatize(mot) for mot in tokkens]

            paires_entraînement.append((tokkens, intent["tag"]))# creer des paires d'entrainement
            all_word.extend(tokkens) # creer un vocabulaire

    all_word = sorted(set(all_word))#rend une liste d'éléments uniques  et trier   

    tags = [intent["tag"] for intent in data["intents"]] # recupere les tag
    tags = sorted(set(tags)) # trier et sans doublon meme si normalement il n'y a pas de doublon si la data est bien faite

    word2idx = { mot : i  for i, mot in enumerate(all_word) }#dictionnaire contenant le mot et un indice
    x_train = []
    y_train = []

    for paire in paires_entraînement :
        temp_list = []
        for token in paire[0]:
            
            if token in all_word:
                i = word2idx[token]
                temp_list.append(i)    
        x_train.append(temp_list)
        y_train.append(paire[1]) # met le tag

    from tensorflow.keras.utils import to_categorical, pad_sequences
    import matplotlib.pyplot as plt 
    from sklearn.model_selection import train_test_split

    for i in range(0, len(y_train)) :# transforme pour rendre ça comprehensible par le modele
        j = tags.index(y_train[i])
        y_train[i]=j

    y = to_categorical(y_train) #modele one hot encoding pour de meilleur performance
    x = pad_sequences(x_train, maxlen=20) #les vecteurs ont maintenant tous la même taille 

    

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    import numpy as np
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    
    with open("./voc.json", "w", encoding="utf-8") as f:
        json.dump(all_word, f, ensure_ascii=False)
    with open("./tags.json", "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False)

        
    #Création du réseaux de neurones
    from keras import layers, Model, optimizers, callbacks
    taille_sequence = len(x_train[0])
    callback = callbacks.EarlyStopping(monitor='val_loss', patience=20, min_delta=0.001, restore_best_weights= True)

    input_layer = layers.Input(shape=(taille_sequence,))

    dropout_layer = layers.Dropout(0.5)

    emb_layer = layers.Embedding(input_dim=len(all_word), output_dim=75)(input_layer)

    lstm_layer = layers.LSTM(64)(emb_layer)

    dense_layer1 = layers.Dense(32, activation='relu')(lstm_layer)

    dense_layer2 = layers.Dense(16, activation='relu')(dense_layer1)

    output_layer = layers.Dense(len(tags), activation='softmax')(dense_layer2)


    # Création du réseau de neurones 
    # à partir des couches
    model = Model(input_layer, output_layer)

    #on prend l'optimiseur adam, la Fonction de perte : categorical_crossentropy et pour les metrics : accuracy
    model.compile(loss='categorical_crossentropy',
                optimizer=optimizers.Adam(),
                metrics=['accuracy'])

    #entrainement du modèle
    history =  model.fit(x=x_train, y=y_train, epochs=200, validation_data=(x_test, y_test), callbacks=[callback], batch_size=8, )

    plt.figure() # Création d'une figure
    plt.plot(history.history['loss'], label='perte') # premiere courbe
    plt.plot(history.history['accuracy'], label='progression') # deuxieme courbe
    plt.legend() # legend

    plt.show() # affiche la figure
    
    dir = "./model_architecture"
    if not os.path.exists(dir):
        os.makedirs(dir)

    version = get_previous_model_version()
    path = dir + "/mon_model_v"+ str(version) + ".keras"
    os.remove(path)
    new_version = int(version) + 1 

    dir = dir + "/mon_model_v"+ str(new_version) + ".keras"
    model.save(dir)