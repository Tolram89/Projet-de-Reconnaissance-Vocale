import os
import speech_recognition as sr
from writting_retranscription import audio_transcribe
from vocal_retranscription import assistant_speech
from word_key_detection import key_word

r=sr.Recognizer()
mic=sr.Microphone()
#print("liste des microphones disponibles :")
#print(sr.Microphone.list_microphone_names()) #afin de trouver le bon index du micro
with mic as source:
    print("Reglage du bruit ambiant...")
    r.adjust_for_ambient_noise(source)
    print("Parlez maintenant...")
    audio = r.listen(source,timeout=100) #timeout pour eviter de bloquer le programme si on ne parle pas
    print("Fin de l'enregistrement.")
with open("audio.wav", "wb") as f:
    f.write(audio.get_wav_data())



resultat = audio_transcribe()
print("Résultat de la transcription :")
print(resultat)

assistant_speech(resultat)
key_word(resultat)

