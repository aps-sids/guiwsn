from model import Data, Session


def add_data(sensor, data):
    s = Session()
    s.add(Data(sensor, data))
    s.commit()
