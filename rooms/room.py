class Room:
    def __init__(self, r_id, r_name, campus, building, timetable):
        self.id = int(r_id)
        self.room_name = r_name
        self.campus= campus 
        self.building = building
        self.timetable = timetable

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.room_name, self.campus, self.building, self.timetable)