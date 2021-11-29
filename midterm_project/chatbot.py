import knowledge
import voice
import display

class Chatbot():
    def __init__(self, disp):
        self.food = knowledge.Food("")
        self.disease = knowledge.Disease()
        self.health = knowledge.Health()
        self.disp = disp

    def start(self):
        prompt = "您好，有關食物營養、找診所、每日建議攝取熱量的問題都可以問我喔"
        voice.chinese_text_to_speech(prompt)

    def food_detail(self):
        while(True):
            prompt = "請說出要查詢的食物"
            display.display_text(self.disp, prompt)
            voice.chinese_text_to_speech(prompt)
            voice.record_speech()
            food_name = voice.chinese_speech_to_text()
            print("使用者說: {}".format(food_name))
            self.food = knowledge.Food(food_name=food_name)        
            if len(self.food.all_find_food().keys()) >= 1 :
                print(self.food.all_find_food().keys())
                break
            else:
                display.display_text(self.disp, "找不到想查詢的食物\n請重新查詢")
                prompt = "找不到想查詢的食物，請重新查詢"
                voice.chinese_text_to_speech(prompt)
        voice.chinese_text_to_speech("找到的食物有")
        for food in self.food.all_find_food().keys():
            show_message = "找到的食品有:\n{}".format(food)
            display.display_text(self.disp, show_message)
            voice.chinese_text_to_speech(food)
        voice.chinese_text_to_speech("請從以上選擇您要選取的食物")
        voice.record_speech()
        selected_food = voice.chinese_speech_to_text()
        print("使用者說: {}".format(selected_food))
        result = self.food.food_detail(selected_food)
        voice.chinese_text_to_speech("該食品每一百公克包含:")
        for key in result:
            show_message = "{}\n{}\n{} {}".format(selected_food, key, result[key][1], result[key][0])
            display.display_text(self.disp, show_message)
            prompt = "{}: {} {}".format(key, result[key][1], result[key][0])
            voice.chinese_text_to_speech(prompt)
        display.display_text(self.disp, "食物資訊結束\n回到主選單")
        voice.chinese_text_to_speech("食物資訊結束，回到主選單")

    
    def disease_detail(self,loc,*syns):
        hospitals = self.disease.find_hospital(loc,*syns)
        voice.chinese_text_to_speech("底下是為您推薦的診所:")
        for hospital in hospitals:
            name = hospital
            address = hospitals[hospital][:11] + '\n' + hospitals[hospital][11:]
            display.display_text(self.disp, "{}\n{}\n{}".format("診所推薦", name, address))
            voice.chinese_text_to_speech("診所名稱: " + hospital)
            voice.chinese_text_to_speech("診所地址: " + hospitals[hospital])


    def health_detail(self):
        while (True):
            if self.health.height ==0:
                display.display_text(self.disp, "請輸入您的身高(公分)")
                voice.chinese_text_to_speech("請輸入您的身高(公分)")
                voice.record_speech()
                height = voice.chinese_speech_to_text()
                print(height)
                self.health.height = int(height)
            elif self.health.weight ==0:
                display.display_text(self.disp, "請輸入您的體重(公斤)")
                voice.chinese_text_to_speech("請輸入您的體重(公斤)")
                voice.record_speech()
                weight = voice.chinese_speech_to_text()
                print(weight)
                self.health.weight = int(weight)
            elif self.health.daily_act ==-1:
                display.display_text(self.disp, "請問您的工作是屬於靜態\n重度體力使用\n或是一般工作類型?")
                voice.chinese_text_to_speech("請問您的工作是屬於靜態\n重度體力使用\n或是一般工作類型?")
                voice.record_speech()
                act = voice.chinese_speech_to_text()
                print(act)
                self.health.recode_act(act)
            else:
                break
        response = "您每日建議攝取的總熱量為\n{}大卡".format(self.health.kcal_recommend() * self.health.weight)
        display.display_text(self.disp, response)
        voice.chinese_text_to_speech(response)