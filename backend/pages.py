from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
import secrets
import string
import requests
import extensibility as ext
from functools import wraps
from pagesUtil import notFoundHTML, serverErrorHTML
from admin import secretariats, rooms, canteens

LOG_URL = "http://127.0.0.1:8084/"
pagesBP = Blueprint("pages", __name__, url_prefix="")

def logAccess(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requests.post(LOG_URL, json = {"accessedURL" : request.url, "clientName" : request.remote_addr})
        return f(*args, **kwargs)
    return decorated

@pagesBP.route("/<microservice>")
@pagesBP.route('/<microservice>/<path:path>', methods=['GET'])  
@logAccess
def generalRoute(microservice, path=""):   
    newmicro = microservices.Microservices()
    if microservice in newmicro.services.keys(): # TODO: asneira se meter mal o URL
        json = newmicro.validateAndParseResponse(newmicro.serviceGet(microservice))
        html = ext.jsontoHTML(json)
        htmlfile = ext.makeHTML("newmicro", html)                      
        return render_template(htmlfile)

    else:
        return render_template("servererrorPage.html")

@pagesBP.route('/room/<identifier>', methods=['GET'])
@logAccess
def showRoom(identifier):
    r_id = int(identifier)

    try:
        room = rooms.getRoom(r_id)

        return render_template("showRoom.html", chosen_room = room, all= room['timetable'])
    except microservices.NotFoundErrorException:
         return notFoundHTML(r_id)

    except microservices.ServerErrorException:
        return serverErrorHTML()

@pagesBP.route("/secretariats/", methods = ["GET"])
@logAccess
def listSecretariatsPage():
    try:
        secretariatsList = secretariats.listSecretariats()

        return render_template("listSecretariats.html", secretariats = secretariatsList)
    except microservices.NotFoundErrorException:
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()

@pagesBP.route("/secretariats/<identifier>", methods = ["GET"])
@logAccess
def getSecretariatPage(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("showSecretariat.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)

    except microservices.ServerErrorException:
        return serverErrorHTML()

@pagesBP.route('/canteen', methods=['GET'])
@logAccess
def canteenlistall():

    try:
        canteen = canteens.apiListMenus()

    except microservices.NotFoundErrorException:
         return render_template("errorPage.html")

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")
    
    else:
        return render_template("listalldays.html", chosen_day = canteen)

@pagesBP.route('/canteen/<identifier>', methods=['GET'])
@logAccess
def canteenShow(identifier):
    c_id = int(identifier)

    try:
        canteen = canteens.getDay(c_id)

    except microservices.NotFoundErrorException:
         return render_template("errorPage.html", id = c_id)

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")
    
    else:
        return render_template("listCanteen.html", chosen_day = canteen)
