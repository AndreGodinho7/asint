from flask import Blueprint, render_template

appBP = Blueprint("app", __name__, url_prefix="")

@appBP.route("/app/")
def appMain():
    return render_template("appMainPage.html")