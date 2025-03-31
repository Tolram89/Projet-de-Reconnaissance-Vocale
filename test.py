import os
import speech_recognition as sr

r=sr.Recognizer()
mic=sr.Microphone()
#print("liste des microphones disponibles :")
#print(sr.Microphone.list_microphone_names()) #afin de trouver le bon index du micro
with mic as source:
    print("Reglage du bruit ambiant...")
    r.adjust_for_ambient_noise(source)
    print("Parlez maintenant...")
    audio = r.listen(source,timeout=3)
with open("audio.wav", "wb") as f:
    f.write(audio.get_wav_data())