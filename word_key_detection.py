import os
def key_word(text):
    if text.count('météo') == 1:
        print("Vous avez dit : météo")
    if text.count('date') == 1:
        print("Vous avez dit : date")
    if text.count('heure')==1:
        print("Vous avez dit : heure")