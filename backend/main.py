from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
from flask import abort
from flask import jsonify
import microservices
import extensibility as ext
import authentication

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

def notFoundHTML(identifier):
    return render_template("errorPage.html", id = identifier), 404

def serverErrorHTML():
    return render_template("servererrorPage.html"), 500

def unauthorizedHTML():
    return render_template("unauthorized.html"), 401

@app.route("/")
def mainPage():
    return "Hello world!"

@app.route("/<microservice>")
@app.route('/<microservice>/<path:path>', methods=['GET'])  
def generalRoute(microservice, path=""):                      
    new_service = microservices.NewService(microservice, )
    
    if microservice in new_service.services.keys():
        newmicro = new_service.getnewMicro()
        html = ext.jsontoHTML(newmicro)
        
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

        return render_template("showRoom.html", chosen_room = room, all= room['timetable'])
    except microservices.NotFoundErrorException:
         return notFoundHTML(r_id)

    except microservices.ServerErrorException:
        return serverErrorHTML()

@app.route("/secretariats/", methods = ["GET"])
def listSecretariatsPage():
    try:
        secretariatsList = secretariats.listSecretariats()

        return render_template("listSecretariats.html", secretariats = secretariatsList)
    except microservices.NotFoundErrorException:
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()

@app.route("/secretariats/<identifier>", methods = ["GET"])
def getSecretariatPage(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("showSecretariat.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)

    except microservices.ServerErrorException:
        return serverErrorHTML()

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
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()

@app.route("/admin/secretariats/create")
@authentication.admin
def createSecretariatForm():
    return render_template("createSecretariatform.html")

@app.route("/admin/secretariats/create", methods=["POST"])
@authentication.admin
def createSecretariat():
    secretariat = secretariats.createSecretariat(dict(request.form))

    return redirect(url_for("getSecretariatPage", identifier = secretariat["id"]))

@app.route("/admin/secretariats/<identifier>/edit")
@authentication.admin
def editSecretariatForm(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("editSecretariatForm.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)
    except microservices.ServerErrorException:
        return serverErrorHTML()

@app.route("/admin/secretariats/<identifier>/edit", methods = ["POST"])
@authentication.admin
def editSecretariat(identifier):
    if "id" not in request.form:
        return render_template("errorPage.html", id = "null"), 400
    
    secretariats.updateSecretariat(identifier, dict(request.form))

    return redirect(url_for('getSecretariatPage', identifier = identifier))

@app.route("/admin/secretariats/<identifier>/delete")
@authentication.admin
def removeSecretariat(identifier):
    try:
        secretariats.deleteSecretariat(identifier)

        return redirect(url_for("listSecretariatsPage"))
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)
    except microservices.ServerErrorException:
        return serverErrorHTML()

@app.route("/admin/createMicroservice")
def createMicroservice():
    pass

if __name__ == '__main__':
    app.run(port=8089)