from flask import Blueprint, render_template
import authentication

appBP = Blueprint("app", __name__, url_prefix="")

@appBP.route("/app/")
@authentication.fenixAuth
def appMain():
    return render_template("appMainPage.html")