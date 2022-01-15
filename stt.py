import speech_recognition as sr

def speech_to_text(filename):
    r = sr.Recognizer()
    media = sr.AudioFile(filename)
    with media as m:
        audio = r.record(m)
    response = r.recognize_google(audio, language="zh-TW")
    return response