from flask import jsonify

class canteenDay:
    def __init__(self,day,meal):
        self.day = day
        self.almoco = []
        self.jantar = []
        for key in meal:
            if key == "Almoço":
                self.almoco = meal[key]
            else:
                self.jantar = meal[key]
    
        
class mealType:
    def __init__(self, tipo, name, menu):
        self.type = tipo
        self.name = name
        self.menu = menu


   
    