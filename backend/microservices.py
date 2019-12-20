import json
import requests
import pickle

SECRETARIATS_SERVICE = "secretariats"
ROOMS_SERVICE = "rooms"
CANTEEN_SERVICE = "canteen"
LOG = "logs" 
NEW_SERVICE = "jnos"
SERVICE_CONFIGURATION = "services.json"

URL_CANTEEN = "127.0.0.1:8080"
URL_ROOMS = "127.0.0.1:8081"
URL_SECRETARIATS = "127.0.0.1:8082"
URL_LOGS = "127.0.0.1:8084"

class ServerErrorException(Exception):
    pass

class ValidationErrorException(Exception):
    pass

class NotFoundErrorException(Exception):
    pass

class Microservices:
    dumpFile = "URLDump.db"
    services = {}
    def __init__(self, name=None, URL=None):
        try:
            f = open(self.dumpFile, 'rb')
            self.services = pickle.load(f)

            if not self.services:
                self.services[ROOMS_SERVICE] = URL_ROOMS
                self.services[SECRETARIATS_SERVICE] = URL_SECRETARIATS
                self.services[CANTEEN_SERVICE] = URL_CANTEEN
                self.services[LOG] = URL_LOGS

            if name is not None and URL is not None:
                self.services[name] = URL
                self.dump()

        except IOError:
            self.dump()
    
    def dump(self):
        f = open(self.dumpFile, 'wb')
        pickle.dump(self.services, f)
        f.close()

    def update(self):
        f = open(self.dumpFile, 'rb')
        self.services = pickle.load(f)

    def validateAndParseResponse(self, response):
        if response.status_code == 404:
            raise NotFoundErrorException()
        
        if response.status_code == 422:
            raise ValidationErrorException()
            
        if int(response.status_code / 100) != 2:
            raise ServerErrorException()

        if response.status_code == 204:
            return None
        
        return response.json()

    def getURL(self, service, identifier = ""):
        return f"http://{self.services[service]}/{identifier}"
    
    def serviceGet(self, service, identifier = ""):
        return requests.get(self.getURL(service, identifier))
    
    def servicePost(self, service, data, identifier = ""):
        return requests.post(self.getURL(service, identifier), json = data)
    
    def servicePut(self, service, data, identifier = ""):
        return requests.put(self.getURL(service, identifier), json = data)

    def serviceDelete(self, service, identifier = ""):
        return requests.delete(self.getURL(service, identifier))

class Rooms(Microservices):
    def getRoom(self, identifier):
        return self.validateAndParseResponse(self.serviceGet(ROOMS_SERVICE, identifier))

class Canteens(Microservices):
    def getDay(self, identifier):
        return self.validateAndParseResponse(self.serviceGet(CANTEEN_SERVICE, identifier))
    
    def apiListMenus(self):
        return self.validateAndParseResponse(self.serviceGet(CANTEEN_SERVICE))

class Secretariats(Microservices):
    def listSecretariats(self):
        return self.validateAndParseResponse(self.serviceGet(SECRETARIATS_SERVICE))
       
    def getSecretariat(self, identifier):
        return self.validateAndParseResponse(self.serviceGet(SECRETARIATS_SERVICE, identifier))

    def createSecretariat(self, secretariat):
        return self.validateAndParseResponse(self.servicePost(SECRETARIATS_SERVICE, secretariat)) 
    
    def updateSecretariat(self, identifier, secretariat):
        return self.validateAndParseResponse(self.servicePut(SECRETARIATS_SERVICE, secretariat, identifier))

    def deleteSecretariat(self, identifier):
        return self.validateAndParseResponse(self.serviceDelete(SECRETARIATS_SERVICE, identifier))

class Logs(Microservices):
    def listlogs(self):
        return self.validateAndParseResponse(self.serviceGet(LOG))