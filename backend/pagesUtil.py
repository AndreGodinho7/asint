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