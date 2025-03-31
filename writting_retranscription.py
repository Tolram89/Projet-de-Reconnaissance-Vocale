import os
import speech_recognition as sr

filename = os.path.join("enregistrements", "test2.wav")

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
            print("Texte reconnu :")
            print(text)
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio. Vérifiez la qualité ou la langue.")
    except sr.RequestError as e:
        print(f"Erreur avec le service de reconnaissance vocale : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")
        
