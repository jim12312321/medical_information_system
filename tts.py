from gtts import gTTS
from time import time
from hashlib import sha256
import os

def hash_sha256(text):
    timecode = time()
    return sha256((str(timecode) + text).encode()).hexdigest()

def text_to_speech(text):
    ## Generate Text-to-Speech data with gTTS
    tts = gTTS(text, lang='zh-TW')
    ## Filename -> Timecode + Response Text, then perform SHA256, take first 8 words
    filename = hash_sha256(text)[:8] + '.mp3'
    tts.save(os.path.join('./response/' + filename))
    return filename