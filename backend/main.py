from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
from flask import abort
from flask import jsonify
import requests
import microservices
import extensibility as ext

app = Flask(__name__)
    
URL_CANTEEN = "127.0.0.1:8080"
URL_ROOMS = "127.0.0.1:8081"
URL_SECRETARIATS = "127.0.0.1:8082"
URL_LOGS = "127.0.0.1:8084"

secretariats = microservices.Secretariats("secretariats", URL_SECRETARIATS)
rooms = microservices.Rooms("rooms", URL_ROOMS)
admin = microservices.Logs("logs", URL_LOGS)

def notFound(message):
    resp = jsonify(error = message)
    resp.status_code = 404
    return resp

@app.route("/")
def mainPage():
    return "Hello world!"

@app.route("/<microservice>")
@app.route('/<microservice>/<path:path>', methods=['GET'])  
def generalRoute(microservice, path=""):   
    micro = microservices.Microservices()

    if microservice in micro.services.keys(): 
        json = micro.validateAndParseResponse(micro.serviceGet(microservice))
        html = ext.jsontoHTML(json)
        htmlfile = ext.makeHTML("newmicro", html)                      
        return render_template(htmlfile)

    else:
        return render_template("servererrorPage.html")

@app.route('/api/room/<identifier>', methods=['GET'])
def apishowRoom(identifier):
    r_id = int(identifier)
    try:
        room = rooms.getRoom(r_id)

        resp = jsonify(room)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, room not found.")

@app.route('/room/<identifier>', methods=['GET'])
def showRoom(identifier):
    r_id = int(identifier)

    try:
        room = rooms.getRoom(r_id)

    except microservices.NotFoundErrorException:
         return render_template("errorPage.html", id = r_id)

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")
    
    else:
        return render_template("showRoom.html", chosen_room = room, all= room['timetable'])

@app.route("/secretariats/", methods = ["GET"])
def listSecretariatsPage():
    try:
        secretariatsList = secretariats.listSecretariats()

        return render_template("listSecretariats.html", secretariats = secretariatsList)
    except microservices.NotFoundErrorException:
        return render_template("errorPage.html", id = request.args["Id"])

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")

@app.route("/secretariats/<identifier>", methods = ["GET"])
def getSecretariatPage(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("showSecretariat.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return render_template("errorPage.html", id = request.args["Id"])

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")

@app.route("/api/secretariats/", methods = ["GET"])
def listSecretariats():
    try:
        secretariatsList = secretariats.listSecretariats()

        resp = jsonify(secretariatsList)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, secretariat not found.")

@app.route("/api/secretariats/<identifier>", methods = ["GET"])
def getSecretariat(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        resp = jsonify(secretariat)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, secretariat not found.")

@app.route("/admin/logs", methods=["GET"])
def listlogs():
    try:
        logList = admin.listlogs()
        return render_template("listLogs.html", logs = logList)

    except microservices.NotFoundErrorException:
        return render_template("errorPage.html", id = request.args["Id"])

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")

@app.route("/admin/secretariat/<identifier>")
def showSecretariat(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("showSecretariat.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        pass
    except microservices.ServerErrorException:
        pass

@app.route("/admin/createSecretariatForm")
def createSecretariatForm():
    return render_template("createSecretariatForm.html")

@app.route("/admin/createSecretariat", methods=["POST"])
def createSecretariat():
    location = request.form["Location"]
    name = request.form["Name"]
    description = request.form["Description"]
    opening_hours = request.form["Opening"] 

    secretariat = {"location":location, "name": name, "description": description, "opening_hours":opening_hours}
    secretariat = admin.createSecretariat(secretariat)

    return render_template("createdSecretariat.html", location=location, 
                                                  name=name, 
                                                  description=description, 
                                                  opening_hours=opening_hours)

@app.route("/admin/editSecretariatForm/<identifier>")
def editSecretariatForm(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("editSecretariatForm.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return render_template("errorPage.html", id = identifier), 404
    except microservices.ServerErrorException:
        return render_template("servererrorPage.html"), 500

@app.route("/admin/editSecretariat", methods = ["POST"])
def editSecretariat():
    if "id" not in request.form:
        return render_template("errorPage.html", id = "null"), 400
    
    secretariats.updateSecretariat(request.form["id"], dict(request.form))

    return redirect(url_for('showSecretariat', identifier = request.form["id"]))

@app.route("/admin/createMicroserviceForm")
def createMicroserviceForm():
    return render_template("createMicroserviceForm.html")

@app.route("/admin/createMicroservice", methods=["POST"])
def createMicroservice():
    url = request.form["URL"]
    name = request.form["Name"]
    
    new_micro = microservices.Microservices(name, url)
    return render_template("createdMicroservice.html", name = name, URL = url)

if __name__ == '__main__':
    app.run(port=8089)