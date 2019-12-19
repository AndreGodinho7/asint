from functools import wraps
from flask import request, Response, session, redirect, url_for

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
        if "userId" not in session.keys() or session['userId'] not in loggedUsers.keys():
            return redirect(url_for("authflow.login"))

        return f(*args, **kwargs)
    return decorated

def loginUser(userId, token):
    loggedUsers[userId] = token
    session["userId"] = userId

def logoutUser():
    del loggedUsers[session["userId"]]
    del session["userId"]

def getUserId():
    return session["userId"]

def getToken():
    return loggedUsers[session["userId"]]