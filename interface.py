import tkinter as tk
from test import run_program

def start_program():
    print("Programme lancé...")
    run_program()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Beru")
root.minsize(600,400)

# Définir la couleur de fond de la fenêtre principale
root.configure(bg="black")

# Création d'un conteneur pour centrer le bouton
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")
# Modifier la couleur de fond du conteneur pour qu'il corresponde
frame.configure(bg="black")

# Ajout d'un bouton pour lancer le programme dans le conteneur
start_button = tk.Button(frame, text="Lancer le programme", command=start_program, font=("Arial", 14))
# Modifier la couleur du bouton pour s'adapter au thème sombre
start_button.configure(bg="gray", fg="white", activebackground="darkgray", activeforeground="white")
start_button.pack()

# Lancement de la boucle principale de l'interface
root.mainloop()
