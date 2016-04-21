#Testing Git
from flask import Flask, request, render_template
import time
import datetime

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

#@app.route("/")
#def hello():
#    return "Jason, you are soooo awesome!"

@app.route("/")
#@app.route("/lab_temp")
def lab_temp():
	import Adafruit_DHT as DHT
	import RPi.GPIO as GPIO
	import sys

	Sensor = 11
	humiture = 17

	humidity, temperature = DHT.read_retry(Sensor, humiture)

	temperature = temperature * 9/5.0 + 32

	if humidity is not None and temperature is not None:
		return render_template("lab_temp.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
	temperatures, humidities, from_date_str, to_date_str = get_records()
	return render_template("lab_env_db.html",temp=temperatures,hum=humidities)

def get_records():
	#Get the from date value from the URL
	from_date_str = request.args.get('from',time.strftime("2016-01-01 00:00"))

	#Get the to date value from the URL
	to_date_str = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))

	# Validate date before sending it to the DB
	if not validate_date(from_date_str):
		from_date_str = time.strftime("%Y-%m-%d 00:00")

	# Validate date before sending it to the DB
	if not validate_date(to_date_str):
		to_date_str	= time.strftime("%Y-%m-%d %H:%M")

	import sqlite3
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM temperatures WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	temperatures 	= curs.fetchall()
	curs.execute("SELECT * FROM humidities WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	humidities 		= curs.fetchall()
	conn.close()
	return [temperatures, humidities, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
