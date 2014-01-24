from flask import render_template
from app.database import db_session
from app.models import Sensor, Data
from app import app


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









