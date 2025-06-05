import tkinter as tk
from tkinter import ttk
from test import run_program
from PIL import Image, ImageTk
import threading # permet de lancer des taches en simultané


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
frame.place(relx=0.5, rely=0.5, anchor="center")
# Modifier la couleur de fond du conteneur pour qu'il corresponde
frame.configure(bg="black")

#Création d'une barre de progression
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
progress.pack(side=tk.TOP, padx=10, pady=10)

# Création d'un bouton image
image_button = tk.Button(frame, image=photo, command=start_program, bg="black", borderwidth=0, activebackground="black") 
#lambda permet de lancer mes deux fonctions en même temps
image_button.image = photo  # Garde une référence à l'image
image_button.pack()

#création d'un bouton pour quitter l'application
button = tk.Button(root, text='Terminer', width=25, command=lambda: [progress.stop(), root.quit()])
button.pack(side=tk.BOTTOM, padx=10 ,pady=10)

# Lancement de la boucle principale de l'interface
root.mainloop()
