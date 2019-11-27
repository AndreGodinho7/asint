import json
import requests

SERVICE_CONFIGURATION = "services.json"

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

    def valroomGet(self, identifier):
        return self.validateAndParseResponse(self.serviceGet("rooms", identifier))