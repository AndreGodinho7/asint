from flask import Flask
from flask import request, redirect, url_for, session
from flask import render_template
from flask import abort
from flask import jsonify
import requests
import microservices
import extensibility as ext
import authentication
import secrets
import string

app = Flask(__name__)
    
app.secret_key = b'\x04`#\xec\xc2\xb1\x89.\xf3\x95\xf4\xe7x\xcaY\x0b'

URL_CANTEEN = "127.0.0.1:8080"
URL_ROOMS = "127.0.0.1:8081"
URL_SECRETARIATS = "127.0.0.1:8082"
URL_LOGS = "127.0.0.1:8084"

secretariats = microservices.Secretariats("secretariats", URL_SECRETARIATS)
rooms = microservices.Rooms("rooms", URL_ROOMS)
admin = microservices.Logs("logs", URL_LOGS)

clientID = "1695915081465956"
clientSecret = "xqedTb5MkSWzIgdFokbiTHtHaJx8rUQgnM2XMMqW2f6TpTrlaknr2kfGV9YyB+Vnve56CTKayrwFbI+U4Sr/RQ=="
redirectURI = "http://projetodojnos.com:8089/userAuth"

fenixLoginPage = f"https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id={clientID}&redirect_uri={redirectURI}"
fenixAccessTokenPage = "https://fenix.tecnico.ulisboa.pt/oauth/access_token"

secretsKeep = {}

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

@app.route("/qrcode")
def render():
    return render_template("qrcode.html")

@app.route("/login")
def login():
    return redirect(fenixLoginPage)

@app.route("/logout")
def logout():
    authentication.logoutUser()
    return redirect("/")

@app.route("/userAuth")
def userAuth():
    code = request.args['code']
    print ("code "+request.args['code'])

    payload = {'client_id': clientID,
               'client_secret': clientSecret,
               'redirect_uri' : redirectURI,
               'code' : code,
               'grant_type': 'authorization_code'}

    response = requests.post(fenixAccessTokenPage, params = payload)

    if response.status_code == 200:
        tokenResponse = response.json()

        token = tokenResponse["access_token"]

        params = {'access_token': token}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        userInformation = resp.json()

        userId = userInformation["username"]

        authentication.loginUser(userId, token)
    else:
        return render_template("serverError.html"), 500

    return redirect(url_for("getSecret"))

@app.route("/secret")
@authentication.fenixAuth
def getSecret():
    loggedUserId = authentication.getUserId()

    for secret, userId in secretsKeep.items():
        if userId == loggedUserId:
            return secret

    newSecret = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                  for i in range(6))

    secretsKeep[newSecret] = loggedUserId

    return newSecret

@app.route("/info/<secret>")
@authentication.fenixAuth
def getInfo(secret):
    if secret not in secretsKeep.keys():
        return notFoundHTML(secret)

    otherUserId = secretsKeep[secret]

    del secretsKeep[secret]

    params = {'access_token': authentication.loggedUsers[otherUserId]}
    resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params) 

    return resp.text

@app.route("/<microservice>")
@app.route('/<microservice>/<path:path>', methods=['GET'])  
def generalRoute(microservice, path=""):   
    micro = microservices.Microservices()

    if microservice in micro.services.keys(): # TODO: asneira se meter mal o URL
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

@app.route("/admin/createMicroserviceForm")
def createMicroserviceForm():
    return render_template("createMicroserviceForm.html")

@app.route("/admin/createMicroservice", methods=["POST"])
def createMicroservice():
    url = request.form["URL"]
    name = request.form["Name"]
    
    new_micro = microservices.Microservices(name, url)
    return render_template("createdMicroservice.html", name = name, URL = url)

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

if __name__ == '__main__':
    app.run(host="192.168.1.85", port=8089)
