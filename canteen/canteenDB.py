import pickle
import dayMenu

class canteenDB:
    def __init__(self,name):
        self.name = name
        try:
            f = open('bd_dump'+name, 'rb')
            self.days = pickle.load(f)
            f.close()
        except IOError:
            self.days = {}

    def createDayMeal(self,date,meal):
        self.days[date] = dayMenu.dayMenu(date,meal)
        f = open('bd_dump' + self.name, 'wb')
        pickle.dump(self.days, f)
        f.close()
        return self.days




