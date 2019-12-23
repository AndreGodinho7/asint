from flask import Blueprint, render_template, request, redirect, jsonify, session
import microservices
import authentication
import secrets
import string
import requests
import extensibility as ext
from functools import wraps
from util import notFoundHTML, serverErrorHTML, logAccess 
from admin import secretariats, rooms, canteens

pagesBP = Blueprint("pages", __name__, url_prefix="")

@pagesBP.route("/<microservice>")
@pagesBP.route('/<microservice>/<path:path>', methods=['GET'])  
@logAccess
def generalRoute(microservice, path=""):   
    newmicro = microservices.Microservices()
    try:
        json = newmicro.validateAndParseResponse(newmicro.serviceGet(microservice))
        html = ext.jsontoHTML(json)
        html = ext.addHeaders(html)                      
        return html

    except KeyError:
        return notFoundHTML(microservice)

    except microservices.ServerErrorException:
        return serverErrorHTML()
    else:
        pass

@pagesBP.route('/rooms/<identifier>', methods=['GET'])
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

@pagesBP.route('/canteen/', methods=['GET'])
@logAccess
def canteenlistall():

    try:
        canteen = canteens.apiListMenus()
        return render_template("listalldays.html", chosen_day = canteen)
    
    except microservices.NotFoundErrorException:
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()
   
       

@pagesBP.route('/canteen/<identifier>', methods=['GET'])
@logAccess
def canteenShow(identifier):
    c_id = int(identifier)

    try:
        canteen = canteens.getDay(c_id)
        return render_template("listCanteen.html", chosen_day = canteen)

    except microservices.NotFoundErrorException:
         return notFoundHTML(c_id)

    except microservices.ServerErrorException:
        return serverErrorHTML()
    
    else:
        pass
