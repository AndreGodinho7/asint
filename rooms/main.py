from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json
import requests
import roomDB

app = Flask(__name__)
db = roomDB.RoomDB("IST Rooms")

def notFound():
    resp = jsonify(error = "Room, not found.")
    resp.status_code = 404
    return resp

@app.route("/", methods = ["GET"])
def listRooms():
    roomsDict = list(map(lambda r: r.__dict__, db.listAllRooms()))
    resp = jsonify(roomsDict)
    resp.status_code = 200
    
    return resp

@app.route('/<identifier>', methods=['GET'])
def getRoom(identifier):
    r_id = str(identifier)

    try: 
        room = db.showRoom(r_id).__dict__
        resp = jsonify(room)
        resp.statusCode = 200
    
    except AttributeError: 
        resp = notFound()

    return resp

if __name__ == '__main__':
    app.run(port=8081)