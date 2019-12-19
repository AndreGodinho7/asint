from flask import Flask
from flask import render_template

from admin import adminBP
from api import apiBP
from secret import secretBP
from pages import pagesBP
from authflow import authflowBP

app = Flask(__name__)
    
app.secret_key = b'\x04`#\xec\xc2\xb1\x89.\xf3\x95\xf4\xe7x\xcaY\x0b'

@app.route("/")
def mainPage():
    return "Hello world!"

@app.route("/qrcode")
def render():
    return render_template("qrcode.html")

app.register_blueprint(adminBP)
app.register_blueprint(apiBP)
app.register_blueprint(secretBP)
app.register_blueprint(pagesBP)
app.register_blueprint(authflowBP)

if __name__ == '__main__':
    app.run(host="192.168.1.85", port=8089)
