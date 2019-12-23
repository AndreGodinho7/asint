from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
from util import logAccess
from admin import secretariats, rooms, canteens

apiBP = Blueprint("api", __name__, url_prefix="")

@apiBP.route("/api/secretariats/", methods = ["GET"])
def listSecretariats():
    try:
        secretariatsList = secretariats.listSecretariats()

        resp = jsonify(secretariatsList)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, secretariat not found.")

@apiBP.route("/api/secretariats/<identifier>", methods = ["GET"])
def getSecretariat(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        resp = jsonify(secretariat)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, secretariat not found.")

@apiBP.route('/api/room/<identifier>', methods=['GET'])
def apishowRoom(identifier):
    r_id = int(identifier)
    try:
        room = rooms.getRoom(r_id)

        resp = jsonify(room)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, room not found.")

@apiBP.route("/api/canteen/", methods = ["GET"])
def apicanteenlistall():

    try:
        canteen = canteens.apiListMenus()
        resp = jsonify(canteen)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, canteen not found.")

@apiBP.route("/api/canteen/<identifier>", methods = ["GET"])
def apicanteenShow(identifier):

    c_id = int(identifier)
    try:
        canteen = canteens.getDay(c_id)
        resp = jsonify(canteen)
        resp.status_code = 200

        return resp
    except microservices.NotFoundErrorException:
        return notFound("Oops, canteen not found.")
