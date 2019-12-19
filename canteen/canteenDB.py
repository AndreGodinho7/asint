import pickle
import canteen
import datetime

class canteenDB:
    def __init__(self,name):
        self.name = name
        try:
            f = open('bd_dump'+name, 'rb')
            f2 = pickle.load(f)
            self.time = f2[0]
            self.days = f2[1]
            f.close()
        except IOError:
            self.days = {}
            self.time = datetime.datetime.now() + datetime.timedelta(hours=2)

    def createDay(self,data):

        meal = self.createDailyMealsDict(data)
        final = canteen.canteenDay(data['day'],meal)
        self.days[data['day']] = final
        f = open('bd_dump' + self.name, 'wb')
        pickle.dump([self.time, self.days], f)
        f.close()
        return final


    def getDayFormat(self,identifier):
        day = None
        c_id = str(identifier)
        if len(c_id)!=8 :
            return day
        day = c_id[:2] + '/' + c_id[2:4] + '/' + c_id[-4:]

        return day

    def createDailyMealsDict(self,data):
         
        final = {}
        for menu in data['meal']:
            refeicoes = []
            for meal in menu['info']:
                x = canteen.mealType(meal['type'], meal['name'], meal['menu'])
                refeicoes.append(x)
                
                final[menu['type']] = refeicoes
        return final

    def getDayMenu(self,data, day):  
        found = None
        for x in data:
            if x["day"] == day:
                found = x
                break
            continue

        return found

    def convert_to_dict(self, obj):
        x = {}
        x["day"] = obj.day
        x["almoco"] = []
        x["jantar"] = []
        for o in obj.almoco:
            x["almoco"].append({"tipo": o.type, "name": o.name, "menu": o.menu})
        for o in obj.jantar:
            x["jantar"].append({"tipo": o.type, "name": o.name, "menu": o.menu})
        return x
    
    def is_there_day(self, day):
        for key in self.days:
            if key == day:
                return True

        return False
    
    def list_all_days(self):
        x = []
        for i in self.days.values():
            x.append(self.convert_to_dict(i))

        return x

    def check_cache(self):
        now = datetime.datetime.now()
        if now > self.time:
            self.time = now + datetime.timedelta(hours=2)
            self.days = {}


                
