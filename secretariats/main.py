from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask import make_response
from functools import wraps
import requests
import secretariatDB

LOG_URL = "http://127.0.0.1:8084/"

app = Flask(__name__)
db = secretariatDB.SecretariatDB() 

def logAccess(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requests.post(LOG_URL, json = {"accessedURL" : request.url, "clientName" : request.remote_addr})
        return f(*args, **kwargs)
    return decorated

def validateCreateSecretariatRequest(createRequest):
    if createRequest == None:
        return False
        
    keys = createRequest.keys()
    return "location" in keys and "name" in keys and "description" in keys and "opening_hours" in keys

def validateEditSecretariatRequest(editRequest):
    return validateCreateSecretariatRequest(editRequest)

def notFound():
    resp = jsonify(error = "Oops, secretariat not found.")
    resp.status_code = 404
    return resp


@app.route("/", methods = ["GET"])
@logAccess
def listSecretariats():
    secretariatsDict = list(map(lambda s: s.__dict__, db.getAll()))
    resp = jsonify(secretariatsDict)
    resp.status_code = 200
    
    return resp

@app.route("/<identifier>", methods = ["GET"])
@logAccess
def getSecretariat(identifier):
    secretariat = db.get(identifier)
    
    if secretariat == None:
        return notFound()

    resp = jsonify(secretariat.__dict__)
    resp.status_code = 200
    
    return resp

@app.route("/", methods = ["POST"])
@logAccess
def createSecretariat():
    if not validateCreateSecretariatRequest(request.json):
        resp = jsonify(error = "Could not create a secretariat due to lack of information.")
        resp.status_code = 422
        return resp
    
    secretariat = db.create(request.json["location"],
                            request.json["name"],
                            request.json["description"],
                            request.json["opening_hours"])

    resp = jsonify(secretariat.__dict__)
    resp.status_code = 201

    return resp

@app.route("/<identifier>", methods = ["PUT"])
@logAccess
def editSecretariat(identifier):
    secretariat = db.get(identifier)

    if secretariat == None:
        return notFound()
    
    if not validateEditSecretariatRequest(request.json):
        resp = jsonify(error = "Could not edit a secretariat due to lack of information.")
        resp.status_code = 422
        return resp

    secretariat.location = request.json["location"]
    secretariat.name = request.json["name"]
    secretariat.description = request.json["description"]
    secretariat.opening_hours = request.json["opening_hours"]
 
    db.dump()

    resp = jsonify(secretariat.__dict__)
    resp.status_code = 200

    return resp

@app.route("/<identifier>", methods = ["DELETE"])
@logAccess
def deleteSecretariat(identifier):
    if db.remove(identifier):
        return make_response("", 204, { "Content-Type" : "application/json" })
    else:
        return notFound()

if __name__ == '__main__':
    app.run(port=8082)