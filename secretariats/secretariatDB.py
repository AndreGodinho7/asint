import pickle
from secretariat import Secretariat

class SecretariatDB:
    def __init__(self):
        try:
            f = open('secretariatDump.db', 'rb')
            self.secretariats = pickle.load(f)
            f.close()
        except IOError:
            self.secretariats = {}

    def getAll(self):
        return self.secretariats.values()

    def get(self, id):
        try:
            return self.secretariats[id]
        except:
            return None

    def create(self, location, name, description, opening_hours):
        new_id = str(len(self.secretariats)) #TODO: change id cretion
        self.secretariats[new_id] = Secretariat(new_id, location, name, description, opening_hours)
        return self.secretariats[new_id]

    def remove(self, id):
        try:
            del self.secretariats[id]
            return True
        except:
            return False