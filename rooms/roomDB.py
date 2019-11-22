import pickle
from room import Room

class RoomDB:
    def __init__(self, name_room):
        self.name = name_room
        try:
            f = open('bd_dump'+name_room, 'rb')
            self.bib = pickle.load(f)
            f.close()
        except IOError:
            self.bib = {}
    
    def createRoom(self, name, r_id, campus, building, timetable):
        self.bib[r_id] = Room(r_id, name, campus, building, timetable)
        f = open('bd_dump' + self.name, 'wb')
        pickle.dump(self.bib, f)
        f.close()
        return self.bib[r_id]

    def showRoom(self, r_id):
        try:
            return self.bib[r_id]
        
        except KeyError:
            return None
    
    def listAllRooms(self):
        return list(self.bib.values())

    def listRoomsCampus(self, campus):
        ret_value = []
        for room in self.bib.values():
            if room.location[0] == campus:
                ret_value.append(room)

    def listRoomsBuilding(self, building):
        ret_value = []
        for room in self.bib.values():
            if room.location[1] == building:
                ret_value.append(room)