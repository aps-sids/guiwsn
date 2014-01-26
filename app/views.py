from flask import render_template
from app.database import db_session
from app.models import Sensor, Data
from app import app
from flask_sockets import Sockets
from sqlalchemy import desc
from json import dumps

sockets = Sockets(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return app.static_folder


@app.route('/sensor')
def home():
    return render_template('sensors.html', sensors=Sensor.query.all())


@app.route('/sensor/<id>')
def sensor(id):
    return render_template('data.html',
                           data=Data.query.filter(Data.sensor_id == id))


@sockets.route('/websocket')
def echo_socket(ws):
    while True:
        message = ws.receive()
        if Sensor.query.filter_by(id=int(message)).count():
            queryr = Data.query.filter_by(sensor_id=int(message)).order_by(desc(Data.time)).limit(100).all()
            ws.send(dumps(map(dict,queryr)))
        else:
            message = "cannot find your thing"
            ws.send(message)
