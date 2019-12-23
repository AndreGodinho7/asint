from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import make_response
from functools import wraps
import requests
import canteenDB

LOG_URL = "http://127.0.0.1:8084/"

app = Flask(__name__)
canteen = canteenDB.canteenDB("canteen")

def logAccess(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requests.post(LOG_URL, json = {"accessedURL" : request.url, "clientName" : request.remote_addr})
        return f(*args, **kwargs)
    return decorated

def getData(url):
    r = requests.get(url)
    data = r.json()
    return data
    
def createDayObject(data):
    obj = canteen.createDay(data["day"],canteen.createDailyMealsDict(data))

def notFound():
    resp = jsonify(error = "Oops, Menu not found.")
    resp.status_code = 404
    return resp

@app.route("/")
@logAccess
def apiListMenus(URL = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"):
    canteen.check_cache()

    if canteen.days:
        pass    
    else:
        data = getData(URL)
        for obj in data:
            canteen.createDay(obj)

    final = canteen.list_all_days()
    resp = jsonify(final)
    resp.statusCode = 200
    return resp

@app.route('/<identifier>', methods=['GET'])
@logAccess
def getDay(identifier, URI = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"):  
    canteen.check_cache()

    day = canteen.getDayFormat(identifier)
    if day==None:
            return notFound()
    if canteen.days:
        pass           
    else:
        data = getData(URI)
        for obj in data:
            canteen.createDay(obj)

    if canteen.is_there_day(day):
        final = canteen.days[day]
        resp = jsonify(canteen.convert_to_dict(final))
        resp.statusCode = 200
        return resp
    else:
        return notFound()

if __name__ == '__main__':
    app.run(port=8080)