from sqlalchemy import (Column, String, ForeignKey,
                        Integer, Float, DateTime)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    range_min = Column(Integer)
    range_max = Column(Integer)
    unit = Column(String(10))

    def __init__(self, type, range_min, range_max, unit):
        self.type = type
        self.range_max = range_max
        self.range_min = range_min
        self.unit = unit

        
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

        
engine = create_engine('sqlite:///sql_alchemy_example.db')
Session = sessionmaker(bind=engine)

#Base.metadata.create_all(engine)
