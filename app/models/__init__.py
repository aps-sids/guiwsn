from sqlalchemy import (Column, String, ForeignKey,
                        Integer, Float, DateTime)
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.database import Base


def todict(self):
    def convert_datetime(value):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    for c in self.__table__.columns:
        if isinstance(c.type, DateTime):
            value = convert_datetime(getattr(self, c.name))
        else:
            value = getattr(self, c.name)

        yield(c.name, value)


def iterfunc(self):
    """Returns an iterable that supports .next()
        so we can do dict(sa_instance)

    """
    return self.todict()

Base.todict = todict
Base.__iter__ = iterfunc


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    range_min = Column(Integer)
    range_max = Column(Integer)
    unit = Column(String(10))

    def __init__(self, type='Digital', range_min=0, range_max=5, unit='V'):
        self.type = type
        self.range_max = range_max
        self.range_min = range_min
        self.unit = unit

    def __repr__(self):
        return "<Sensor:id {} type {}>".format(self.id, self.type)


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    value = Column(Float)
    time = Column(DateTime)
    sensor = relationship("Sensor", backref=backref('data', order_by=id))

    def __init__(self, sensor_id, value):
        self.sensor_id = sensor_id
        self.time = datetime.now()
        self.value = value

    def __repr__(self):
        return "<Data: id {} sensor {} value {} >".format(self.id,
                                                          self.sensor_id,
                                                          self.value)
