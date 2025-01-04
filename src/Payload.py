import json


class Payload:

    def __init__(self, inbound_id:int, settings:dict):
        self.inbound_id:int = inbound_id
        self.settings:dict = settings


    def format(self):
        return {"inbound" : self.inbound_id, "settings": json.dumps(self.settings)}