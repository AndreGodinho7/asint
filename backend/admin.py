from flask import Blueprint, render_template, request, url_for, redirect
import microservices
import authentication

secretariats = microservices.Secretariats()
rooms = microservices.Rooms()
canteen = microservices.Canteens()
admin = microservices.Logs()

adminBP = Blueprint("admin", __name__, url_prefix="")

def notFoundHTML(identifier):
    return render_template("errorPage.html", id = identifier), 404

def serverErrorHTML():
    return render_template("servererrorPage.html"), 500

def unauthorizedHTML():
    return render_template("unauthorized.html"), 401

@adminBP.route("/admin/logs", methods=["GET"])
def listlogs():
    try:
        logList = admin.listlogs()
        return render_template("listLogs.html", logs = logList)

    except microservices.NotFoundErrorException:
        return notFoundHTML("")

    except microservices.ServerErrorException:
        return serverErrorHTML()

@adminBP.route("/admin/secretariats/create")
@authentication.admin
def createSecretariatForm():
    return render_template("createSecretariatform.html")

@adminBP.route("/admin/secretariats/create", methods=["POST"])
@authentication.admin
def createSecretariat():
    secretariat = secretariats.createSecretariat(dict(request.form))

    return redirect(url_for("pages.getSecretariatPage", identifier = secretariat["id"]))

@adminBP.route("/admin/secretariats/<identifier>/edit")
@authentication.admin
def editSecretariatForm(identifier):
    try:
        secretariat = secretariats.getSecretariat(identifier)

        return render_template("editSecretariatForm.html", secretariat = secretariat)
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)
    except microservices.ServerErrorException:
        return serverErrorHTML()

@adminBP.route("/admin/secretariats/<identifier>/edit", methods = ["POST"])
@authentication.admin
def editSecretariat(identifier):
    if "id" not in request.form:
        return render_template("errorPage.html", id = "null"), 400
    
    secretariats.updateSecretariat(identifier, dict(request.form))
    return redirect(url_for('pages.getSecretariatPage', identifier = identifier))

@adminBP.route("/admin/createMicroserviceForm")
def createMicroserviceForm():
    return render_template("createMicroserviceForm.html")

@adminBP.route("/admin/createMicroservice", methods=["POST"])
def createMicroservice():
    url = request.form["URL"]
    name = request.form["Name"]
    
    new_micro = microservices.Microservices(name, url)
    return render_template("createdMicroservice.html", name = name, URL = url)

@adminBP.route("/admin/secretariats/<identifier>/delete")
@authentication.admin
def removeSecretariat(identifier):
    try:
        secretariats.deleteSecretariat(identifier)

        return redirect(url_for("pages.listSecretariatsPage"))
    except microservices.NotFoundErrorException:
        return notFoundHTML(identifier)
    except microservices.ServerErrorException:
        return serverErrorHTML()