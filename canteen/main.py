from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import requests
import dayMenu
import canteenDB

app = Flask(__name__)
canteen = canteenDB.canteenDB("canteen")

def getData(url):
    r = requests.get(url)
    data = r.json()
    return data
    

def getDayFormat(identifier):
    
    day = None
    c_id = str(identifier)
    if len(c_id)!=8 :
        return day

    day = c_id[:2] + '/' + c_id[2:4] + '/' + c_id[-4:]
    return day

def getDayMenu(data, day):  
    
    found = None
    for x in data:
        if x["day"] == day:
            found = x
            break
        continue

    return found

def createDayObject(data):
    obj = canteen.createDayMeal(data["day"],data)

def notFound():
    resp = jsonify(error = "Oops, Menu not found.")
    resp.status_code = 404
    return resp

@app.route("/Menus")
def apiListMenus():
    URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
    r = requests.get(url = URL)
    data = r.json()
    resp = jsonify(data)
    resp.statusCode = 200
    return resp

@app.route('/Menus/<identifier>', methods=['GET'])
def getDay(identifier, URI = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"):
    
    data = getData(URI)
    day = getDayFormat(identifier)

    if day==None:
        return notFound()
    
    try:
        meal = canteen.days[day].meal
        print("hello")
    except:
        meal = getDayMenu(data,day)
        if meal== None:
            return notFound()
        else:
            createDayObject(meal)
            
    resp = jsonify(meal)
    resp.statusCode = 200
    return resp

if __name__ == '__main__':
    app.run(port=8080)

    