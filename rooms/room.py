class Room:
    def __init__(self, r_id, r_name, campus, building, timetable):
        self.id = r_id
        self.name = r_name
        self.location = (campus, building)
        self.timetable = timetable

    def __str__(self):
        return "{} {} {} {} ".format(self.id, self.name, self.location, self.timetable)