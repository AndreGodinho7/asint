from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from functools import wraps
import json
import requests
import roomDB
import datetime

LOG_URL = "http://127.0.0.1:8084/"
ROOM_URL = "http://127.0.0.1:8082/"


app = Flask(__name__)
db = roomDB.RoomDB()

def logAccess(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requests.post(LOG_URL, json = {"accessedURL" : request.url, "clientName" : request.remote_addr})
        return f(*args, **kwargs)
    return decorated

def notFound():
    resp = jsonify(error = "Room not found.")
    resp.status_code = 404
    return resp

@app.route("/", methods = ["GET"])
@logAccess
def listRooms(): 
    roomsDict = list(map(lambda r: r.__dict__, db.listAllRooms()))
    resp = jsonify(roomsDict)
    resp.status_code = 200
    
    return resp

@app.route('/<identifier>', methods=['GET'])
@logAccess
def getRoom(identifier):
    r_id = str(identifier)
    now = datetime.datetime.now()

    try: 
        room = db.showRoom(r_id, now).__dict__
        resp = jsonify(room)
        resp.statusCode = 200
    
    except AttributeError: 
        resp = notFound()

    return resp


if __name__ == '__main__':
    app.run(port=8081)