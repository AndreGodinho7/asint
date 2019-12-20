from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
import secrets
import string
import requests
from datetime import datetime, timedelta

from pagesUtil import notFoundHTML

secretBP = Blueprint("secret", __name__, url_prefix="")

class Secret:
    def __init__(self, secret, userId, expires):
        self.secret = secret
        self.userId = userId
        self.expires = expires

def generateNewSecret(userId):
    newSecret = ''.join(secrets.choice(string.ascii_uppercase + string.digits) 
                                                for i in range(6))
    secretsKeep[newSecret] = Secret(newSecret, userId, datetime.now() + timedelta(minutes=2))

    return newSecret

secretsKeep = {}

@secretBP.route("/secret")
@authentication.fenixAuth
def getSecret():
    loggedUserId = authentication.getUserId()

    for secret, userId in secretsKeep.items():
        if userId.userId == loggedUserId:
            return secret

    return generateNewSecret(loggedUserId)

@secretBP.route("/info/<secret>")
@authentication.fenixAuth
def getInfo(secret):
    if secret not in secretsKeep.keys():
        return notFoundHTML(secret)

    secretKept = secretsKeep[secret]
    del secretsKeep[secret]

    if datetime.now() > secretKept.expires:
        return notFoundHTML(secret)

    otherUserId = secretKept.userId
    params = {'access_token': authentication.loggedUsers[otherUserId].token}
    resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params) 

    return resp.text