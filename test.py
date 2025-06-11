import speech_recognition as sr
from writting_retranscription import audio_transcribe
from vocal_retranscription import assistant_speech
from speak_chatbot import speak_with_chatbot

def run_program():
    r = sr.Recognizer()
    mic = sr.Microphone()
    #print("liste des microphones disponibles :")
    #print(sr.Microphone.list_microphone_names()) #afin de trouver le bon index du micro
    with mic as source:
        print("Reglage du bruit ambiant...")
        r.adjust_for_ambient_noise(source)
        print("Parlez maintenant...")
        audio = r.listen(source,timeout=5, phrase_time_limit=100) #timeout pour eviter de bloquer le programme si on ne parle pas
        print("Fin de l'enregistrement.")
    with open("audio.wav", "wb") as f:
        f.write(audio.get_wav_data())



    resultat = audio_transcribe()
    print("Résultat de la transcription :")
    print(resultat)
    if resultat != "" :
        reponse = speak_with_chatbot(resultat)
    else :
        reponse = "Vous n'avez rien dit"
    assistant_speech(reponse)