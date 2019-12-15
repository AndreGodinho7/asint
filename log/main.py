from flask import Flask
from flask import request, make_response
from flask import abort
from flask import jsonify

import logDB

app = Flask(__name__)
db = logDB.LogDB() 

def validateCreateLogRequest(createRequest):
    if createRequest == None:
        return False

    #TODO: Validate datetime strings!
    keys = createRequest.keys()
    return "accessedURL" in keys and "clientName" in keys

def validateEditLogRequest(editRequest):
    return validateCreateLogRequest(editRequest)

def notFound():
    resp = jsonify(error = "Oops, log not found.")
    resp.status_code = 404
    return resp

@app.route("/", methods = ["GET"])
def listLogs():
    logsDict = list(map(lambda s: s.__dict__, db.getAll()))
    resp = jsonify(logsDict)
    resp.status_code = 200
    
    return resp

@app.route("/<identifier>", methods = ["GET"])
def getLog(identifier):
    log = db.get(identifier)
    
    if log == None:
        return notFound()

    resp = jsonify(log.__dict__)
    resp.status_code = 200
    
    return resp

@app.route("/", methods = ["POST"])
def createLog():
    if not validateCreateLogRequest(request.json):
        resp = jsonify(error = "Could not create a log due to lack of information.")
        resp.status_code = 422
        return resp

    user = None

    if "user" in request.json.keys():
        user = request.json["user"]    
    
    log = db.create(request.json["accessedURL"],
                            request.json["clientName"],
                            user)

    resp = jsonify(log.__dict__)
    resp.status_code = 201

    return resp

@app.route("/<identifier>", methods = ["PUT"])
def editLog(identifier):
    log = db.get(identifier)

    if log == None:
        return notFound()
    
    if not validateEditLogRequest(request.json):
        resp = jsonify(error = "Could not edit a log due to lack of information.")
        resp.status_code = 422
        return resp

    log.accessedURL = request.json["accessedURL"]
    log.accessDate = request.json["accessDate"]
    log.clientName = request.json["clientName"]

    if "user" in request.json.keys():
        log.user = request.json["user"]
 
    db.dump()

    resp = jsonify(log.__dict__)
    resp.status_code = 200

    return resp

@app.route("/<identifier>", methods = ["DELETE"])
def deleteLog(identifier):
    if db.remove(identifier):
        return make_response("", 204, { "Content-Type" : "application/json" })
    else:
        return notFound()

if __name__ == '__main__':
    app.run(port=8084)