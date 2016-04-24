import sqlite3
import sys
import Adafruit_DHT as DHT

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	curs=conn.cursor()
	curs.execute("""INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

#Sensor = 11
#humiture = 17

#humidity, temperature = DHT.read_retry(Sensor, humiture)

# If you don't have a sensor but still wish to run this program, comment out all the
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
import random
humidity = random.randint(1,100)
temperature = random.randint(10,30)

temperature = temperature * 9/5.0 + 32

if humidity is not None and temperature is not None:
	log_values("1", temperature, humidity)
else:
	log_values("1", -999, -999)
