from gtts import gTTS
import socket
import urllib
import os
import speech_recognition as sr
from dotenv import load_dotenv
import time
import threading
import socket
import struct
import re
import os
import sys
from subprocess import call
from enum import Enum, unique
from traceback import print_exc
from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

Lab = AudioFormat(sample_rate_hz=16000, num_channels=1, bytes_per_sample=2)

LANG="TW"

# Load environmental variable
load_dotenv('.env')

def askForService(token, data, output_file, model="F06"):
    HOST = "140.116.245.146"
    PORT = 10012
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    received = ""
    try:
        sock.connect((HOST, PORT))
        msg = bytes(token+"@@@"+data+"@@@"+model, "utf-8")
        msg = struct.pack(">I", len(msg)) + msg
        sock.sendall(msg)
        
        with open(output_file,'wb') as f:
            while True:
                l = sock.recv(8192)
                if not l: break
                f.write(l)
        print("File received complete")
    finally:
        sock.close()
    print("Result saved at {}.".format(output_file))
    return "OK"

def taiwanese_text_to_speech(data, output_file):
    token = os.getenv("TAIWANESE_STT_TOKEN")
    result = askForService(token,data, output_file)
    return result

def record_speech():
    # Onboard pin 32 as button
    # Use pin 34 as GND
	with Board(button_pin=12) as board:
		print('請按下按鈕開始錄音.')
		board.button.wait_for_press()
		done = threading.Event()
		board.button.when_pressed = done.set
		
		def wait():
			start = time.monotonic()
			while not done.is_set():
				duration = time.monotonic() - start
				print('錄音中: %.02f 秒 [按下按鈕停止錄音]' % duration)
				time.sleep(0.5)
		
		record_file(Lab, filename='./static/recording.wav', wait=wait, filetype='wav')

def chinese_speech_to_text():
    wav_file = './static/recording.wav'
    r = sr.Recognizer()
    with sr.WavFile(wav_file) as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language='zh-tw')
        return result
    except LookupError:
        print("Could not understand audio:" , wav_file)
        return None

def chinese_text_to_speech(text):
    tts = gTTS(text = text, lang = 'zh-tw')
    tts.save("./static/output.mp3")
    os.system("mpg321 -q ./static/output.mp3")
    return