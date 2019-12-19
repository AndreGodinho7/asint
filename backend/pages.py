from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
import secrets
import string
import requests
import extensibility as ext
from pagesUtil import notFoundHTML, serverErrorHTML

pagesBP = Blueprint("pages", __name__, url_prefix="")

URL_CANTEEN = "127.0.0.1:8080"
URL_ROOMS = "127.0.0.1:8081"
URL_SECRETARIATS = "127.0.0.1:8082"
URL_LOGS = "127.0.0.1:8084"

secretariats = microservices.Secretariats("secretariats", URL_SECRETARIATS)
rooms = microservices.Rooms("rooms", URL_ROOMS)
admin = microservices.Logs("logs", URL_LOGS)

@pagesBP.route("/<microservice>")
@pagesBP.route('/<microservice>/<path:path>', methods=['GET'])  
def generalRoute(microservice, path=""):   
    micro = microservices.Microservices()

    if microservice in micro.services.keys(): # TODO: asneira se meter mal o URL
        json = micro.validateAndParseResponse(micro.serviceGet(microservice))
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
        return serverErrorHTML()