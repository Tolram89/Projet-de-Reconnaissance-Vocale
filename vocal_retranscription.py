from gtts import gTTS
import os
import playsound


def assistant_speech(text):
    """ :
    Fonction pour faire parler l'assistant vocal.
    Utilise gTTS pour convertir le texte en audio et playsound pour lire le fichier audio.
    """
    # Vérifier si le texte est vide
    if not text:
        print("Le texte est vide. Aucune action effectuée.")
        return
    # Vérifier si le texte est une chaîne de caractères
    if not isinstance(text, str):
        print("Le texte doit être une chaîne de caractères.")
        return
    tts = gTTS(text, lang='fr', tld='fr') 
    tts.save('output.mp3')
    playsound.playsound("output.mp3", True)
    os.remove("output.mp3")
