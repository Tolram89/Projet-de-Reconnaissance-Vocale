from gtts import gTTS
import os
import playsound



def assistant_speech(text, langue_parler):
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
    if langue_parler=="ar" or langue_parler=="zh" or langue_parler=="ja" or langue_parler=="en":
        tts = gTTS(text, lang=langue_parler) # utlisier gTTS 
    else: 
        tts = gTTS(text, lang=langue_parler, tld=langue_parler)
    langue_parler="fr"
    tts.save('output.mp3')
    playsound.playsound("output.mp3", True)
    os.remove("output.mp3")
