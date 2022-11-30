from .application import db


class Bus(db.Document):
    _id = db.ObjectIdField()
    start = db.ArrayField()
    end = db.ArrayField()
    stops = db.ArrayField()
    time = db.ArrayField()
    current_location = db.ArrayField()

    def __init__(self, _id, start, end, stops, time, current_location):
        self._id = _id
        self.start = start
        self.end = end
        self.stops = stops
        self.time = time
        self.current_location = current_location


def delete_all():
    try:
        Bus.objects({}).delete()
        print("Delete All Done!")
    except Exception as e:
        print("failed " + str(e))
