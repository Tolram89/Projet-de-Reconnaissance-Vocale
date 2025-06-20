import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps  # Ajout de ImageOps
import threading # permet de lancer des taches en simultané
import sounddevice
import soundfile as sf
from writting_retranscription import audio_transcribe
from vocal_retranscription import assistant_speech
from speak_chatbot import speak_with_chatbot
import numpy as np

recording = False
audio_frames = []
fs = 16000  # fréquence d'échantillonnage
label2 = None #pour pouvoir l'effacer correctement


def on_image_button_click():
    global recording, audio_frames, label2
    if not recording:
        progress.start() # Démarrer la barre de progression
        recording = True
        audio_frames = []
        label2=tk.Label(root,text="Enregistrement en cours, \n appuyer à nouveau pour stopper l'enregistrement", font=("Terminal", 20), bg="black", fg="green")
        label2.pack(side=tk.BOTTOM, padx=10, pady=10)
        threading.Thread(target=record_audio).start()
    else:
        recording = False# arrete l'enregistrement
        label2.pack_forget()  # Effacer le texte du label avant de commencer l'enregistrement
        progress.stop() # stopper la barre de progression

def record_audio():
    global audio_frames, recording
    def callback(indata, frames, time, status):
        if recording:
            audio_frames.append(indata.copy())
        else:
            raise sounddevice.CallbackStop()
    with sounddevice.InputStream(samplerate=fs, channels=1, callback=callback):
        while recording:
            sounddevice.sleep(100)
    # Sauvegarde et transcription
    audio_np = np.concatenate(audio_frames, axis=0)
    sf.write("audio.wav", audio_np, fs)
    label2 = tk.Label(root,text="Fin de l'enregistrement.", font=("Terminal", 20), bg="black", fg="green")
    label2.pack(side=tk.BOTTOM, padx=10, pady=10)
    label2.after(2000, label2.destroy)  # Détruire le label après 2 secondes
    print("Enregistrement terminé.")
    resultat = audio_transcribe()
    print("Résultat de la transcription :")
    print(resultat)
    run_program(resultat)


def run_program(resultat):
    if resultat != "" :
        reponse, langue_cible = speak_with_chatbot(resultat)
    elif resultat == None:
        pass#ne rien faire pour pouvoir reparler
    else :
        reponse = "Vous n'avez rien dit, vérifier que votre micro fonctionne bien"
        langue_cible="fr"
    assistant_speech(reponse, langue_cible)

def resize_image(event):
    # Utiliser la taille du frame pour calculer la taille du bouton
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    size = min(frame_width, frame_height) // 3  #adapte la taille
    if size < 50:#taille minimum
        size = 50
    img_resized = img.resize((size, size))
    photo_resized = ImageTk.PhotoImage(img_resized)
    image_button.config(image=photo_resized)
    image_button.image = photo_resized  # Garde la référence


# Création de la fenêtre principale
root = tk.Tk()
root.title("Beru")
root.minsize(600,400)

# Définir la couleur de fond de la fenêtre principale
root.configure(bg="black")

# Chargement de l'image
image_path = "oreil prog.jpg" 
img = Image.open(image_path)
img = img.resize((150, 150))  # Redimensionner si besoin

# Inverser les couleurs de l'image
img = img.convert("RGB")  # S'assurer que l'image est en mode RGB
img = ImageOps.invert(img)

photo = ImageTk.PhotoImage(img)


#création d'un bouton pour quitter l'application
button = tk.Button(root, text='Terminer', width=25, command=lambda: [progress.stop(), root.quit()])
button.pack(side=tk.BOTTOM, padx=10, pady=10)

#Création d'une barre de progression
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.pack(side=tk.BOTTOM, padx=10, pady=10)

# Création d'un label pour le texte
label1 =tk.Label(root, text="Bienvenue dans l'assistant vocal Beru", font=("Terminal", 20), bg="black", fg="green")
label1.pack(side=tk.TOP, padx=10, pady=10)

# Création d'un conteneur pour centrer le bouton
frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

# Modifier la couleur de fond du conteneur pour qu'il corresponde
frame.configure(bg="black")

# Création d'un bouton image
image_button = tk.Button(frame, image=photo, command=on_image_button_click, bg="black", borderwidth=0, activebackground="black") 
#lambda permet de lancer mes deux fonctions en même temps
image_button.image = photo  # Garde une référence à l'image
image_button.pack(expand=True)

frame.bind("<Configure>", resize_image)

# Lancement de la boucle principale de l'interface
root.mainloop()
