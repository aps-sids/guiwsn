


class DataProvider:
    """
    Subclass this and make a usable read function and provide a
    logging interval
    """
    from random import random
    def read(self):
        return random()*5

    
class SensorLogger():

    def __init__(self, object,model, session, interval=1):
        if not isinstance(object, DataProvider):
            raise TypeError("DataProvider object required")
        self.dp = object
        self.interval = interval

    def log(self):

        from ..app.models import Data
        from time import sleep
        while True:
            data = self.dp.read()
            session.add(Data(sensor_id, data))
            session.commit()
            sleep(interval)
            
    
        
