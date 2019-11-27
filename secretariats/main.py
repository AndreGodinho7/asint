from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import requests

app = Flask(__name__)

@app.route("/")
def apiListMenus():
    URL = "https://fenixedu.org/dev/api/#get-canteen"
    r = requests.get(url = URL)
    data = r.json()
    print(data)

    #return "Hello world!"

if __name__ == '__main__':
    app.run(port=8082)