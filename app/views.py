from flask import render_template, redirect
from app.database import db_session
from app.models import Sensor, Data
from app import app
from flask_sockets import Sockets
from sqlalchemy import desc
from json import dumps
from time import sleep
import random

sockets = Sockets(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def redirectToFirstSensor():
    return redirect('/1')


@app.route('/<id>')
def index(id):
    if Sensor.query.filter_by(id=id).count():
                queryr = Data.query.filter_by(sensor_id=id).order_by(desc(Data.time)).limit(100).all()
                data = map(dict, queryr)
                values = [e["value"] for e in data]
                #times = [e["time"][-8:] for e in data]
                values2 = values[:]
                random.shuffle(values2)
    return render_template('graph.html', values=values, values2=values2)
    #return app.static_folder


@app.route('/sensor')
def home():
    return render_template('sensors.html', sensors=Sensor.query.all())


@app.route('/sensor/<id>')
def sensor(id):
    return render_template('data.html',
                           data=Data.query.filter(Data.sensor_id == id))

@app.route('/sensor/data/<id>')
def sensordata(id):
    if Sensor.query.filter_by(id=id).count():
                queryr = Data.query.filter_by(sensor_id=id).order_by(desc(Data.time)).limit(100).all()
                return dumps(map(dict, queryr))
    



@sockets.route('/websocket')
def echo_socket(ws):
    message = ws.receive()
    ws.send(message)
    while True:
        if message is not None:
            if Sensor.query.filter_by(id=int(message)).count():
                queryr = Data.query.filter_by(sensor_id=int(message)).order_by(desc(Data.time)).limit(100).all()
                ws.send(dumps(map(dict, queryr)))
                sleep(2)
        
