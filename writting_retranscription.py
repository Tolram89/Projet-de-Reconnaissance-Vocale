import os
import speech_recognition as sr


#transformer cette partie en fonction
def audio_transcribe(filename = "audio.wav") :
    """
    Transcrit un fichier audio en texte en utilisant l'API Google Speech Recognition.

    Args:
        filename (str): Chemin vers le fichier audio à transcrire.

    Returns:
        str: Texte transcrit ou message d'erreur.
    """
    recognizer = sr.Recognizer()

    if not os.path.exists(filename):
        print(f"Le fichier audio '{filename}' est introuvable.")
    else:
        try:
            with sr.AudioFile(filename) as source:
                print("Chargement de l'audio...")
                audio_data = recognizer.record(source)
                print("Reconnaissance en cours...")
                text = recognizer.recognize_google(audio_data, language="fr-FR")
                return text  # Retourne le texte transcrit
        except sr.UnknownValueError:
            return "Impossible de comprendre l'audio. Vérifiez la qualité ou la langue."
        except sr.RequestError as e:
            return f"Erreur avec le service de reconnaissance vocale : {e}"
        except Exception as e:
            return f"Une erreur inattendue s'est produite : {e}"
            

