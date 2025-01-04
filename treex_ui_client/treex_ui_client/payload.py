import json
import pprint


class Payload:

    def __init__(self, inbound_id:int, settings:dict):
        self.inbound_id:int = inbound_id
        self.settings:dict = settings


    def format(self):
        return {"inbound" : self.inbound_id, "settings": json.dumps(self.settings)}

    def __str__(self):
        return f'Inbound: {self.inbound_id},\nSettings: {pprint.pformat(self.settings)}'

    def __repr__(self):
        return f'Payload(inbound_id= {self.inbound_id}, settings={pprint.pformat(self.settings)} )'