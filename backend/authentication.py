from functools import wraps
from flask import request, Response, session, redirect, url_for
from datetime import datetime

class Principal:
    def __init__(self, userId, token, expires):
        self.userId = userId
        self.token = token
        self.expires = expires
        

loggedUsers = {}

def admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not(request.authorization and request.authorization["username"] == "admin" and request.authorization["password"] == "admin"):
            resp = Response()
            resp.headers["WWW-Authenticate"] = "Basic"

            return resp, 401
        return f(*args, **kwargs)
    return decorated

def fenixAuth(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if "userId" not in session.keys() or getUserId() not in loggedUsers.keys():
            return redirect(url_for("authflow.login"))

        if datetime.today() > loggedUsers[getUserId()].expires:
            logoutUser()
            return redirect(url_for("authflow.login"))

        return f(*args, **kwargs)
    return decorated

def loginUser(userId, token, expires):
    loggedUsers[userId] = Principal(userId, token, expires)
    session["userId"] = userId

def logoutUser():
    del loggedUsers[getUserId()]
    del session["userId"]

def getUserId():
    return session["userId"]

def getToken():
    return loggedUsers[getUserId()].token