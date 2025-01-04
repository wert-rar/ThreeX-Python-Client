class ClientError(Exception):
    def __int__(self, text,status):
        self.txt = text
        self.status = status

    def __repr__(self):
        return f'ClientError:  {self.txt} \nstatus: [{self.status}]'