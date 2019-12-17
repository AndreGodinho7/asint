from functools import wraps
from flask import request, Response

def admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not(request.authorization and request.authorization["username"] == "admin" and request.authorization["password"] == "admin"):
            resp = Response()
            resp.headers["WWW-Authenticate"] = "Basic"

            return resp, 401
        return f(*args, **kwargs)
    return decorated