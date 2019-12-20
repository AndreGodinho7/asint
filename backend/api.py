from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
from pagesUtil import notFound
from admin import secretariats, rooms, canteen

apiBP = Blueprint("api", __name__, url_prefix="")

@apiBP.route("/api/microservices", methods = ["GET"])
def listMicroservices():
    services = microservices.Microservices().services

    resp = jsonify(services)
    resp.status_code = 200
    
    return resp

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