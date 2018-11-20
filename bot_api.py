import requests,json,time
class ErrorCreateBot(Exception):
    def __init__(self):
        print("Ошибка при подключении к боту, проверьте токен!")
class Bot():
    def __init__(self,token):
        self.token = token
        self.req = self.apiRequests("getMe")
        if bool(self.req['ok']):
            print("Подключение к боту произведено успешно")
            self.run()
        else:
            raise ErrorCreateBot
    def response_msg(self,chat_id,text):
        req = self.apiRequests("sendMessage",chat_id=chat_id,text=text)
        print("[%s] Ответ пользователю %s: %s" %(self.uptd_id,self.from_user,text))

    def time(self):
        t = time.localtime()
        hour = t[3]
        min = t[4]
        if hour>=6 and hour<12:
            return "Доброе утро, время -"+str(hour)+":"+str(min)
        elif hour>=12 and hour<18:
            return "Добрый день, время -"+str(hour)+":"+str(min)
        elif hour>=18 and hour<24:
            return "Добрый вечер, время -"+str(hour)+":"+str(min)
        elif hour<6:
            return "Пора спать, время -"+str(hour)+":"+str(min)
    def commands(self,command,chat_id):
        if command == "/time":
            msg = self.time()
        elif command == "/lol":
            msg = "Ха-ха, смешно"
        elif command == "/start":
            msg = "Добро пожаловать!"
        elif command == "/error":
            msg = "Что бы сообщить об ошибке, напишите создателю бота: @Lolipop223"
        else:
            msg = "Не понимаю о чём идёт речь :с"

        self.response_msg(chat_id,msg)
    def open_info(self):
        f = open("%s" % self.req["result"]["username"],"r")
        text = f.readline()
        lupdt = text.split(":")
        self.uptd_id = lupdt[1]


    def run(self):
        try:
            self.open_info()
            temp = self.uptd_id
            while True:
                req = self.apiRequests("getUpdates")
                if req["result"][-1]["update_id"] != temp:
                    temp = req["result"][-1]["update_id"]
                    self.uptd_id = req["result"][-1]["update_id"]
                    self.from_user = req["result"][-1]["message"]["from"]["username"]
                    text_msg = req["result"][-1]["message"]["text"]
                    print("[%s] %s, написал сообщение: %s" % (self.uptd_id,self.from_user,text_msg))
                    self.commands(req["result"][-1]["message"]["text"],req["result"][-1]["message"]["chat"]["id"])
                    self.save_info()
        except:
            pass



    def save_info(self):
        f = open("%s" % self.req["result"]["username"],"w")
        f.write("lupt:%s" % self.uptd_id)
    def apiRequests(self,method,**arg):
        try:
            url = ("https://api.telegram.org/bot%s/%s" % (self.token,method))
            req = requests.session()
            res = req.get(url=url,params=arg)
            txt = json.loads(res.text)
            return txt
        except:
            print("Ошибка подключения")

my_bot = Bot("796825899:AAGNh6TZX889dhBa7ChGVH2RhGgvut2SrW0")
