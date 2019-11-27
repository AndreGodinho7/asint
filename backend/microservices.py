import json
import requests

SERVICE_CONFIGURATION = "services.yaml"
SECRETARIATS_SERVICE = "secretariats"

class ServerErrorException(Exception):
    pass

class ValidationErrorException(Exception):
    pass

class NotFoundErrorException(Exception):
    pass

class Microservices:
    def __init__(self):
        with open(SERVICE_CONFIGURATION, 'r') as file:
            self.services = json.load(file)

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
    
    def serviceGet(self, service, identifier = ""):
        return requests.get(f"http://{self.services[service]}/{identifier}")
    
    def servicePost(self, service, data, identifier = ""):
        return requests.post(f"http://{self.services[service]}/{identifier}", json = data)
    
    def servicePut(self, service, data, identifier = ""):
        return requests.put(f"http://{self.services[service]}/{identifier}", json = data)

    def serviceDelete(self, service, identifier = ""):
        return requests.delete(f"http://{self.services[service]}/{identifier}")
    
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