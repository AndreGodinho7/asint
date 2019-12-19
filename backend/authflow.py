from flask import Blueprint, render_template, request, redirect
import microservices
import authentication
import secrets
import string
import requests
from datetime import timedelta, datetime

authflowBP = Blueprint("authflow", __name__, url_prefix="")

clientID = "1695915081465956"
clientSecret = "xqedTb5MkSWzIgdFokbiTHtHaJx8rUQgnM2XMMqW2f6TpTrlaknr2kfGV9YyB+Vnve56CTKayrwFbI+U4Sr/RQ=="
redirectURI = "http://projetodojnos.com:8089/userAuth"

fenixLoginPage = f"https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id={clientID}&redirect_uri={redirectURI}"
fenixAccessTokenPage = "https://fenix.tecnico.ulisboa.pt/oauth/access_token"

@authflowBP.route("/login")
def login():
    return redirect(fenixLoginPage)

@authflowBP.route("/logout")
def logout():
    authentication.logoutUser()
    return redirect("/")

@authflowBP.route("/userAuth")
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
        secondsUntilExpiration = int(tokenResponse["expires_in"])

        expirationDate = datetime.today() + timedelta(seconds=secondsUntilExpiration)

        params = {'access_token': token}
        resp = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person", params = params)

        userInformation = resp.json()

        userId = userInformation["username"]

        authentication.loginUser(userId, token, expirationDate)
    else:
        return render_template("serverError.html"), 500

    return redirect("/")