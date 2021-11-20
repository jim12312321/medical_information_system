import knowledge

class Chatbot():
    def __init__(self):
        self.food = knowledge.Food("")
        self.disease = knowledge.Disease()
        self.health = knowledge.Health()

    def start(self):
        return "您好，我是小白，有關食物營養、找診所、每日建議攝取熱量的問題都可以問我喔！"

    def food_detail(self):
        while(True):
            food_name = input("請輸入要查詢的食物:")
            self.food = knowledge.Food(food_name=food_name)        
            if len(self.food.all_find_food().keys()) >= 1 :
                print(self.food.all_find_food().keys())
                break
            else:
                print("找不到您想查詢的食物，請重新輸入")            
        selected_food = input("請從以上選擇您要選取的食物並輸入：")
        self.food.food_detail(selected_food)
    
    def disease_detail(self,loc,*syns):
        print(self.disease.find_hospital(loc,*syns))

    def health_detail(self):
        while (True):
            if self.health.height ==0:
                self.health.recode_height(int(input("請輸入您的身高(公分):")))
            elif self.health.weight ==0:
                self.health.recode_weight(int(input("請輸入您的體重(公斤):")))
            elif self.health.daily_act ==-1:
                self.health.recode_act(input("請問您的工作屬於靜態、重度體力使用或是一般工作類型呢?:"))
            else:
                break
        print("您每日建議攝取的總熱量為{}大卡".format(self.health.kcal_recommend()))

if __name__ == '__main__': 
    chatbot = Chatbot()
    print(chatbot.start())
    result = input("請選擇食品營養、找診所或是每日推薦攝取熱量:")
    if "食品" in result or "營養" in result:
        chatbot.food_detail()
    elif "找" in result or "診所" in result:
        loc = input("請問搜尋的地區:")
        syns = input("請問您的症狀:")
        chatbot.disease_detail(loc,syns)
    elif "建議" in result or "熱量" in result:
        chatbot.health_detail()
    else:
        print("尚未支援此項功能")