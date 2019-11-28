from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask import jsonify
import microservices

app = Flask(__name__)

api = microservices.Microservices()

@app.route("/")
def mainPage():
    return "Hello world!"

@app.route('/api/room/<identifier>', methods=['GET'])
def showRoom(identifier):
    r_id = int(identifier)

    try:
        room = api.getRoom(r_id)

    except microservices.NotFoundErrorException:
        return render_template("errorPage.html", id = request.args["Id"])

    except microservices.ServerErrorException:
        return render_template("servererrorPage.html")
    
    else:
        return render_template("showRoom.html", chosen_room = room, all= room['timetable'])

if __name__ == '__main__':
    app.run(port=8089)