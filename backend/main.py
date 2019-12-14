from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask import jsonify
import microservices
import extensibility as ext

app = Flask(__name__)

secretariats = microservices.Secretariats()
rooms = microservices.Rooms()
new_services = []

def notFound(message):
    resp = jsonify(error = message)
    resp.status_code = 404
    return resp

@app.route("/")
def mainPage():
    return "Hello world!"

@app.route('/<microservice>/<path:path>', methods=['GET']) # TODO: discutir se é melhor assim ou só 
def generalRoute(microservice, path):                      # com <microservice:microservice>
    new_service = microservices.NewService()
    
    if microservice in new_service.services.keys():
        new_services.append(new_service) # TODO: fará sentido ir guardado em lista? 

        newmicro = new_service.getnewMicro()
        html = ext.jsontoHTML(newmicro)
        
        htmlfile = ext.makeHTML("newmicro", ext.HTML_INIT+html+ext.HTML_FINAL)

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

if __name__ == '__main__':
    app.run(port=8089)