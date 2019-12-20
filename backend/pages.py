from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
import secrets
import string
import requests
import extensibility as ext
from pagesUtil import notFoundHTML, serverErrorHTML
from admin import secretariats, rooms, canteen

pagesBP = Blueprint("pages", __name__, url_prefix="")

@pagesBP.route("/<microservice>")
@pagesBP.route('/<microservice>/<path:path>', methods=['GET'])  
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
def listSecretariatsPage():
    try:
        secretariatsList = secretariats.listSecretariats()

        return render_template("listSecretariats.html", secretariats = secretariatsList)
    except microservices.NotFoundErrorException:
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()

@pagesBP.route("/secretariats/<identifier>", methods = ["GET"])
def getSecretariatPage(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("showSecretariat.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)

    except microservices.ServerErrorException:
<<<<<<< HEAD
        return serverErrorHTML()
=======
        return serverErrorHTML()

@pagesBP.route('/canteen', methods=['GET'])
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
>>>>>>> 26b050d884dab5990f85ea4cb7f2900626a168cc
