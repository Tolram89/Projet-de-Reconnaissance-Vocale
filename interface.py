import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import threading
import sounddevice
import soundfile as sf
import numpy as np

recording = False
audio_frames = []
fs = 16000  # fréquence d'échantillonnage
label2 = None  # (ligne 2, pour les messages d'enregistrement)

# --- FONCTIONS DE L'INTERFACE ---

def preload_ia_modules():
    progress.config(mode="determinate", maximum =100, value = 0)
    #Charge les modules IA lourds en arrière-plan.
    from writting_retranscription import audio_transcribe
    progress['value'] = 25
    from vocal_retranscription import assistant_speech
    progress['value'] = 50
    from speak_chatbot import speak_with_chatbot
    progress['value'] = 75

def show_image_button():
    #Affiche le bouton image après le chargement des modules IA.
    global img, image_button
    image_path = "oreil prog.jpg"
    img = Image.open(image_path)
    img = img.resize((100, 100))
    img = img.convert("RGB")
    img = ImageOps.invert(img)
    photo = ImageTk.PhotoImage(img)
    image_button = tk.Button(frame, image=photo, command=on_image_button_click, bg="black", borderwidth=0, activebackground="black")
    image_button.image = photo
    image_button.pack(expand=True)
    frame.bind("<Configure>", resize_image)

def finish_loading():
    #Retire le label de chargement et affiche le bouton image.
    progress['value'] = 0
    progress.config(mode="indeterminate")
    loading_label.destroy()
    show_image_button()

def threaded_preload():
    #Lance le préchargement des modules IA dans un thread séparé.
    preload_ia_modules()
    root.after(0, finish_loading)# appelle la fonction dès que le thread est fini

def on_image_button_click():
    #Gère le clic sur le bouton image (enregistrement audio).
    global recording, audio_frames, label2
    if not recording:
        progress.start()
        recording = True
        audio_frames = []
        show_label2("Enregistrement en cours, appuyer à nouveau pour stopper l'enregistrement")
        threading.Thread(target=record_audio).start()
    else:
        recording = False
        hide_label2()
        progress.stop()

def record_audio():
    #Enregistre l'audio et lance la transcription.
    from writting_retranscription import audio_transcribe
    global audio_frames, recording
    def callback(indata, frames, time, status):
        if recording:
            audio_frames.append(indata.copy())
        else:
            raise sounddevice.CallbackStop()
    with sounddevice.InputStream(samplerate=fs, channels=1, callback=callback):
        while recording:
            sounddevice.sleep(100)
    audio_np = np.concatenate(audio_frames, axis=0)
    sf.write("audio.wav", audio_np, fs)
    show_label2("Fin de l'enregistrement.")
    label2.after(2000, hide_label2)
    print("Enregistrement terminé.")
    resultat = audio_transcribe()
    print("Résultat de la transcription :")
    print(resultat)
    run_program(resultat)

def run_program(resultat):
    #Lance le chatbot et la synthèse vocale selon la transcription.
    from speak_chatbot import speak_with_chatbot
    from vocal_retranscription import assistant_speech
    if resultat != "":
        reponse, langue_cible = speak_with_chatbot(resultat)
    elif resultat is None:
        return
    else:
        reponse = "Vous n'avez rien dit, vérifier que votre micro fonctionne bien"
        langue_cible = "fr"
    assistant_speech(reponse, langue_cible)

def resize_image(event):
    #Redimensionne dynamiquement l'image du bouton selon la taille du frame.
    frame_width = frame.winfo_width()
    frame_height = frame.winfo_height()
    size = min(frame_width, frame_height) // 3
    if size < 50:
        size = 50
    img_resized = img.resize((size, size))
    photo_resized = ImageTk.PhotoImage(img_resized)
    image_button.config(image=photo_resized)
    image_button.image = photo_resized

# --- INTERFACE GRAPHIQUE ---

root = tk.Tk()
root.title("Beru")
root.minsize(854, 480)
root.configure(bg="black")

# Configuration du grid principal (4 lignes, 2 colonne)
root.rowconfigure(0, weight=0)  # label1 (fixe)
root.rowconfigure(1, weight=1)  # frame central (prend tout l'espace dispo)
root.rowconfigure(2, weight=0)  # label2 (fixe)
root.rowconfigure(3, weight=0)  # progress
root.rowconfigure(4, weight=0)  # bouton
root.columnconfigure(0, weight=1)

# Label d'accueil (ligne 0)
label1 = tk.Label(root, text="Bienvenue dans l'assistant vocal Beru", font=("Terminal", 20), bg="black", fg="green")
label1.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Frame central pour le bouton image (ligne 1)
frame = tk.Frame(root, bg="black")
frame.grid(row=1, column=0, sticky="nsew")

# Frame pour label2 (ligne 2)
frame_label2 = tk.Frame(root, bg="black", height=50)  # hauteur fixe
frame_label2.grid(row=2, column=0, columnspan=2, sticky="ew")
frame_label2.grid_propagate(False)  # Empêche le frame de changer de taille

# Label de chargement (affiché au lancement, dans le frame central)
loading_label = tk.Label(frame, text="Chargement en cours...", font=("Terminal", 20), bg="black", fg="yellow")
loading_label.pack(expand=True)

# Bouton pour quitter l'application (ligne 3, colonne 1)
button = tk.Button(root, text='Terminer', width=25, command=lambda: [progress.stop(), root.quit()])
button.grid(row=4, column=0, sticky="", padx=10, pady=10)

# Barre de progression (ligne 3, colonne 0)
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.grid(row=3, column=0, sticky="", padx=10, pady=10)

# Pour afficher/détruire label2 proprement :
def show_label2(text):
    global label2
    if label2:
        label2.destroy()
    label2 = tk.Label(root, text=text, font=("Terminal", 20), bg="black", fg="green")
    label2.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

def hide_label2():
    global label2
    if label2:
        label2.destroy()
        label2 = None

# Lancer le préchargement des modules IA en arrière-plan
threading.Thread(target=threaded_preload, daemon=True).start()

# Boucle principale
root.mainloop()