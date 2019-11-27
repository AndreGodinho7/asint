class room:
    def __init__(self, r_id, campus, building, timetable):
        self.id = r_id
        self.location = (campus, building)
        self.timetable = timetable

    def __str__(self):
        return "{} {} {} ".format(self.id, self.location, self.timetable)