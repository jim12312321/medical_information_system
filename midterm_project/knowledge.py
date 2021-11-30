import requests
from bs4 import BeautifulSoup

class Food():
    def __init__(self,food_name):
        self.food = food_name
        self.food_dict = {}
        self.detail = ["熱量","水分","總碳水化合物","蛋白質","鈉"]

    def parser(self,RUL,food):
        response = requests.get(RUL+food)
        soup = BeautifulSoup(response.text,"html.parser")    
        return soup

    #所有跟欲搜尋食物有關連的食物   
    def all_find_food(self):        
        soup = self.parser('https://consumer.fda.gov.tw/Food/TFND.aspx?nodeID=178&k=',self.food)
        results = soup.find_all("a")
        for result in results:
            if self.food in result.getText():
                current_food = result.getText()
                try:
                    current_food=current_food.replace('(','')
                    current_food=current_food.replace(')','')
                except:
                    pass
                self.food_dict[current_food] = result.get("href")
        return self.food_dict
    
    #該食物的營養資訊
    def food_detail(self,selected_food):
        soup = self.parser('https://consumer.fda.gov.tw/Food/',self.food_dict[selected_food])
        results = soup.find_all("td")
        nutrient_detail = dict()
        for result in results:
            for nutrient in self.detail:
                if nutrient == result.getText():
                    #print("分析項:{}".format(result.getText()))
                    nutrient_detail[nutrient] = []
                    next_node = result.find_next_siblings("td")
                    for element in next_node:
                        if "單位" == element.get("data-th"):
                            #print("單位:{}".format(element.getText()))
                            nutrient_detail[nutrient].append(element.getText())
                        elif "每100克含量" in element.get("data-th"):
                            #print("每100克含量:{}".format(element.getText()))
                            nutrient_detail[nutrient].append(element.getText())
                            break #避免後面重複
        return nutrient_detail

class Disease():
    def __init__(self):
        self.disease_name = ''
        self.hospital = ['診所','醫院']

    def enter_disease_name(self,name):
        self.disease_name = name
    
    #醫院順序會依照評價排序
    def find_hospital(self,loc,*syns):
        hospital_dict = {}
        temp = {}
        RUL = 'https://www.google.com.tw/maps/search/'+loc+'+'
        for syn in syns:
            RUL += syn+"+"
        RUL = RUL.strip('+')
        print(RUL)
        response = requests.get(RUL) 
        results = response.text.split("\\\"")
        for result in results:
            if "業主" in result:
                continue
            for h_type in self.hospital:
                if h_type in result:
                    if result not in temp.keys() and "號" not in result:
                        temp[result] = ''
                    if "號" in result:
                        temp[result.split("號")[1]] = result.split("號")[0]+"號"
        
        for k,i in temp.items():
            if i != '':
               hospital_dict[k] = i 

        
        return hospital_dict

class Health():
    def __init__(self):
        self.height = 0
        self.weight = 0
        self.daily_act = -1 # 0->輕度, 1 ->中度, 2->重度, -1->尚未設定
        self.daily_kcal = 0 #累積kcal

    def recode_weight(self,w):
        self.weight = w

    def recode_height(self,h):
        self.height = h

    #result 接收工作種類 藉此判斷每日活動量
    #0 -> mild, 1->moderate, 2->severe
    def recode_act(self,result:list or str):
        if "靜態" in result or "坐著" in result:
            self.daily_act = 0
        elif "重度" in result:
            self.daily_act = 2
        else:
            self.daily_act = 1
        
    
    # 0->under, 1->normal, 2->over
    def bmi(self): 
        b = self.weight/(self.height/100)**2
        if b>24:
            return 2
        elif b>18.5:
            return 1
        else:
            return 0

    #建議每天攝取熱量
    def kcal_recommend(self):
        #以下計算之資料來源：https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=544&pid=726
        h_class = self.bmi()
        assert self.daily_act != -1
        need_kcal = 35 + 5*self.daily_act - 5*h_class
        return need_kcal


if __name__ =='__main__':
    # 食物查詢的範例
    '''
    while(True):
        food_name = input("請輸入要查詢的食物:")
        food = Food(food_name=food_name)        
        if len(food.all_find_food().keys()) >= 1 :
            print(food.all_find_food().keys())
            break
        else:
            print("找不到您想查詢的食物，請重新輸入")            
    selected_food = input("請從以上選擇您要選取的食物並輸入：")
    food.food_detail(selected_food)
    '''

    #醫院查詢的範例
    '''
    disease = Disease()
    print(disease.find_hospital("高雄湖內","肌肉痠痛"))
    '''
