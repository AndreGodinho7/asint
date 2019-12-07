import pickle
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
import json
import requests
from room import Room
import datetime

URI_room = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"

class TimeOut(Exception):
        pass

def get_json(URI):
    r = requests.get(URI)
    node = r.json()
    return node

def get_building(node):
    """
    Gets the building of the room by recursively accessing parents info 
    """
    if node["parentSpace"]["type"] == 'BUILDING':
        return node["parentSpace"]["name"]

    else:
        id_parent = node["parentSpace"]["id"]
        URI = URI_room + id_parent
        node = get_json(URI)
        building = get_building(node)

    return building

class RoomDB:
    def __init__(self, name_room):
        self.name = name_room
        try:
            f = open('bd_dump'+name_room, 'rb')
            self.rooms = pickle.load(f)
            f.close()
        except IOError:
            self.rooms = {}
    
    def createRoom(self, name, r_id, campus, building, timetable, timer):
        self.rooms[r_id] = Room(r_id, name, campus, building, timetable, timer)
        f = open('bd_dump' + self.name, 'wb')
        pickle.dump(self.rooms, f)
        f.close()
        return self.rooms[r_id]

    def showRoom(self, r_id, cur_time):
        try:
            if self.rooms[r_id].timer < cur_time: # Cache TimeOut
                del self.rooms[r_id]
                raise TimeOut
            
            room = self.rooms[r_id]

            timetable = []
            for slot in room.timetable:
                data_time = datetime.datetime.strptime(slot['day'], '%d/%m/%Y')
                if data_time.day == cur_time.day and data_time.month == cur_time.month:
                    timetable.append(slot)    
            room.timetable = timetable
            return room
        
        except (KeyError, TimeOut):            
            URI = URI_room + r_id 
            room = get_json(URI)
            
            if "error" in room.keys(): # if wrong identifier is inserted 
                if room["error"] == "id not found":
                    return None
                                
            building = get_building(room)
                
            if not room['events']: # if events -> timetable is empty
                timetable = []

            else:
                timetable = room['events']
                
                for i in range(len(timetable)):
                    if timetable[i]['type'] == "LESSON":
                        for key, value in timetable[i]['course'].items():
                            if key == 'name':
                                key = 'title'
                            timetable[i][key] = value
                        
                        del timetable[i]['course']

            room = self.createRoom(room["name"],
                                    room["id"],
                                    room["topLevelSpace"]["name"],
                                    building,
                                    timetable,
                                    cur_time + datetime.timedelta(hours=2))
            return room

    def listAllRooms(self):
        return list(self.rooms.values())

    def listRoomsCampus(self, campus):
        ret_value = []
        for room in self.rooms.values():
            if room.location[0] == campus:
                ret_value.append(room)

    def listRoomsBuilding(self, building):
        ret_value = []
        for room in self.rooms.values():
            if room.location[1] == building:
                ret_value.append(room)