import json
import requests

SERVICE_CONFIGURATION = "services.yaml"

class ServerErrorException(Exception):
    pass

class ValidationErrorException(Exception):
    pass

class Microservices:
    def __init__(self):
        with open(SERVICE_CONFIGURATION, 'r') as file:
            self.services = json.load(file)
    def listSecretariats(self):
        response = requests.get(f"http://{self.services['secretariats']}/")

        if response.status_code != 200:
            return None

        return response.json()