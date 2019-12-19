from flask import Blueprint, render_template, request, redirect, jsonify
import microservices
import authentication
import secrets
import string
import requests

from pagesUtil import notFoundHTML

secretBP = Blueprint("secret", __name__, url_prefix="")

secretsKeep = {}

@secretBP.route("/secret")
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

@secretBP.route("/info/<secret>")
@authentication.fenixAuth
def getInfo(secret):
    if secret not in secretsKeep.keys():
        return notFoundHTML(secret)

    otherUserId = secretsKeep[secret]

    del secretsKeep[secret]

    params = {'access_token': authentication.loggedUsers[otherUserId]}
    resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params) 

    return resp.text