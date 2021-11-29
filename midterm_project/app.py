import RPi.GPIO as GPIO
import time
import os
import display
import voice
import sensor

from chatbot import Chatbot

from board import SCL, SDA
import busio
import adafruit_ssd1306

i2c = busio.I2C(SCL,SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
disp.rotation = 2
disp.fill(0)
disp.show()

started = False

chatbot = None

def main():
    global started
    while(True):
        if started == False:
            dist = sensor.distance()
            if(dist < 30):
                prompt = "機器人開始"
                display.display_text(disp, prompt)
                chatbot = Chatbot(disp)
                chatbot.start()
                started = True
            else:
                prompt = "距離太遠\n更靠近感應器"
                display.display_text(disp, prompt)
        else:
            prompt = "選單"
            prompt = "請選擇食品營養\n找診所或是\n每日推薦攝取熱量"
            display.display_text(disp, prompt)
            voice.chinese_text_to_speech(prompt)
            voice.record_speech()
            user_response = voice.chinese_speech_to_text()
            print("使用者說: {}".format(user_response))
            if "食品" in user_response or "營養" in user_response:
                chatbot.food_detail()
            elif "找" in user_response or "診所" in user_response:
                display.display_text(disp, "請告知搜尋的地區")
                voice.chinese_text_to_speech("請告知搜尋的地區")
                voice.record_speech()
                loc = voice.chinese_speech_to_text()
                print("使用者說: {}".format(loc))
                display.display_text(disp, "請說出您的症狀")
                voice.chinese_text_to_speech("請說出您的症狀")
                voice.record_speech()
                syns = voice.chinese_speech_to_text()
                print("使用者說: {}".format(syns))
                chatbot.disease_detail(loc,syns)
            elif "建議" in user_response or "熱量" in user_response:
                chatbot.health_detail()
            else:
                display.display_text(disp, "尚未支援此項功能")
                voice.chinese_text_to_speech("尚未支援此功能")

if __name__ == '__main__':
    main()