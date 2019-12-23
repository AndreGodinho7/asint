from flask import render_template, jsonify

def notFoundHTML(identifier):
    return render_template("errorPage.html", id = identifier), 404

def serverErrorHTML():
    return render_template("servererrorPage.html"), 500

def unauthorizedHTML():
    return render_template("unauthorized.html"), 401

def notFound(message):
    resp = jsonify(error = message)
    resp.status_code = 404
    return resp

def logAccess(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = {"accessedURL" : request.url, "clientName" : request.remote_addr}

        if "userId" in session.keys():
            data["user"] = session["userId"]

        requests.post(LOG_URL, json = data)

        return f(*args, **kwargs)
    return decorated