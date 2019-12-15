from datetime import datetime
import pickle

class Log:
    def __init__(self, identifier, accessedURL, clientName, user = None):
        self.identifier = identifier
        self.accessedURL = accessedURL
        self.logDate = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
        self.clientName = clientName
        self.user = user

class LogDB:
    dumpFile = "logDump.db"
    def __init__(self):
        try:
            f = open(self.dumpFile, 'rb')
            self.logs = pickle.load(f)
            f.close()
        except IOError:
            self.logs = {}

    def dump(self):
        f = open(self.dumpFile, 'wb')
        pickle.dump(self.logs, f)
        f.close()

    def getAll(self):
        return self.logs.values()

    def get(self, id):
        try:
            return self.logs[id]
        except:
            return None

    def create(self, accessedURL, clientName, user = None):
        new_id = str(len(self.logs)) #TODO: change id cretion
        self.logs[new_id] = Log(new_id, accessedURL, clientName, user)
        self.dump()
        return self.logs[new_id]

    def remove(self, id):
        try:
            del self.logs[id]
            self.dump()
            return True
        except:
            return False