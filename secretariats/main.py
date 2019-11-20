from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def mainPage():
    return "Hello world!"

if __name__ == '__main__':
    app.run(port=8082)