from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json
import requests

URI_shuttle = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/shuttle"

app = Flask(__name__)

def get_json(URI):
    r = requests.get(URI)
    node = r.json()
    return node


@app.route("/")
def shuttle():
    shuttle = get_json(URI_shuttle)

    resp = jsonify(shuttle)
    resp.status_code = 200

    return resp


if __name__ == '__main__':
    app.run(port=8090)