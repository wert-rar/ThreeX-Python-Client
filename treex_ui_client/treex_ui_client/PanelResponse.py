import json
import pprint


class PanelResponse:
    """
    Class for representing a response from the Panel API.
    """
    def __init__(self, response):
        self.success = response.get('success', False)
        self.message = response.get('message', '')
        self.obj = response.get('obj', None)
        if self.obj is not None:
            self.obj = json.loads(self.obj)

    def __repr__(self):
        return ('PanelResponse object (\n'
                f'success : {self.success}\n'
                f'msg : {self.message}\n'
                f'obj : {pprint.pformat(self.obj)}\n)')

