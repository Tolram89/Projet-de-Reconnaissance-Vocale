import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading # permet de lancer des taches en simultané
import os
import speech_recognition as sr
from writting_retranscription import audio_transcribe
from vocal_retranscription import assistant_speech
from word_key_detection import key_word

def run_program():
    r = sr.Recognizer()
    mic = sr.Microphone()
    #print("liste des microphones disponibles :")
    #print(sr.Microphone.list_microphone_names()) #afin de trouver le bon index du micro
    with mic as source:
        print("Reglage du bruit ambiant...")
        # Création d'un label pour d texte
        label2 = tk.Label(root,text="Reglage du bruit ambiant...", font=("Arial", 16), bg="blue")
        label2.pack(side=tk.BOTTOM, padx=10, pady=10)
        r.adjust_for_ambient_noise(source)
        print("Parlez maintenant...")
        label2.pack_forget()  # Effacer le texte du label avant de commencer l'enregistrement
        label2=tk.Label(root,text="Parlez maintenant...", font=("Arial", 16), bg="blue")
        label2.pack(side=tk.BOTTOM, padx=10, pady=10)
        audio = r.listen(source,timeout=5, phrase_time_limit=100) #timeout pour eviter de bloquer le programme si on ne parle pas
        print("Fin de l'enregistrement.")
        label2.pack_forget()  # Effacer le texte du label après l'enregistrement
        label2 = tk.Label(root,text="Fin de l'enregistrement.", font=("Arial", 16), bg="blue")
        label2.pack(side=tk.BOTTOM, padx=10, pady=10)
        label2.after(2000, label2.destroy)  # Détruire le label après 2 secondes
    with open("audio.wav", "wb") as f:
        f.write(audio.get_wav_data())



    resultat = audio_transcribe()
    print("Résultat de la transcription :")
    print(resultat)
    reponse=key_word(resultat)
    assistant_speech(reponse)


def start_program():
    print("Programme lancé...")
    progress.start() # Démarrer la barre de progression
    root.update()  # Force l'affichage de la barre
    threading.Thread(target=run_and_stop_progress).start() # Lancer la fonction dans un thread séparé


def run_and_stop_progress():
    run_program() # Lancer la fonction qui exécute le programme
    progress.stop() # Arrêter la barre de progression


# Création de la fenêtre principale
root = tk.Tk()
root.title("Beru")
root.minsize(600,400)

# Définir la couleur de fond de la fenêtre principale
root.configure(bg="white")

# Chargement de l'image
image_path = "oreil prog.jpg" 
img = Image.open(image_path)
img = img.resize((150, 150))  # Redimensionner si besoin
photo = ImageTk.PhotoImage(img)

# Création d'un conteneur pour centrer le bouton
frame = tk.Frame(root)
frame.place(x=300, y=175, anchor="center")  # Centrer le conteneur dans la fenêtre

# Modifier la couleur de fond du conteneur pour qu'il corresponde
frame.configure(bg="black")

#création d'un bouton pour quitter l'application
button = tk.Button(root, text='Terminer', width=25, command=lambda: [progress.stop(), root.quit()])
button.pack(side=tk.BOTTOM, padx=10, pady=10)

#Création d'une barre de progression
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.pack(side=tk.BOTTOM, padx=10, pady=10)

# Création d'un bouton image
image_button = tk.Button(frame, image=photo, command=start_program, bg="black", borderwidth=0, activebackground="black") 
#lambda permet de lancer mes deux fonctions en même temps
image_button.image = photo  # Garde une référence à l'image
image_button.pack()

# Création d'un label pour afficher du texte
label1 =tk.Label(root, text="Bienvenue dans l'assistant vocal Beru", font=("Arial", 16), bg="blue")
label1.pack(side=tk.TOP, padx=10, pady=10)


# Lancement de la boucle principale de l'interface
root.mainloop()
