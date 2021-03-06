# import necessary libraries
import os
import smtplib
import picamera
import json
import requests
from sparkpost import SparkPost
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from nanpy import (ArduinoApi, SerialManager)
from time import sleep
# get text message json data here
firebase_url = 'https://fireberrypi.firebaseio.com/.json'
r = requests.get(firebase_url)
data = json.loads(r.text)
sp = SparkPost(API_KEY)  #Insert your API Key in ' ' here 
carrier = data['carrier']
# email = data['test2']['email']
# email_password = data['test2']['email_password']
name = data['name']
phone_number = str(data['phone_number'])
pi_lat = str(39.244881)
pi_long = str(-77.266147)
# pi_lat = str(data['latitude'])
# pi_long = str(data['longitude'])

# get android phone location here
firebase_location_url = 'https://fireberrylocation.firebaseio.com/.json'
r1 = requests.get(firebase_location_url)
data1 = json.loads(r1.text)
phone_lat = str(data1['latitude'])
phone_long = str(data1['longitude'])

peopleExist = False

def determine_people():
	print (pi_lat, phone_lat)
	print (pi_long, phone_long)
	if float(phone_lat) > 39 and float(phone_long) < -77:
		peopleExist = True
	else:
		peopleExist = False
	return peopleExist

def determine_carrier_email():
	email_to_send = ''

	if carrier == 'att':
		email_to_send = phone_number + '@mms.att.net'
	elif carrier == 'sprint':
		email_to_send = phone_number + '@messaging.sprintpcs.com'
	elif carrier == 'tmobile':
		email_to_send = phone_number + '@tmomail.net'
	elif carrier == 'verizon':
		email_to_send = phone_number + '@vtext.com'
	else:
		print("please select a valid carrier")

	return email_to_send
def SendSpMail(ImgFileName):
	sendEmail = determine_carrier_email()
	people = determine_people()
	
	if(people == True):
		response = sp.transmissions.send(
			recipients=[sendEmail],
			from_email='mail@mail.shahv98.me',
			subject='Gas Alert',
			text=name+', an abnormal amount of gas has been identified. According to the registered phones location, there is 1 person near the FireBerryPi',
			track_opens=True,
			track_clicks=True,
			attachments=[{"name":"capture.jpg","type":"image/jpeg","filename":ImgFileName}]
		)
	else:
		 response = sp.transmissions.send(
			recipients=[sendEmail],
			from_email='mail@mail.shahv98.me',
			subject='Gas Alert',
			text=name+', an abnormal amount of gas has been identified. According to the registered phones location, there are no known people near the FireBerryPi',
			track_opens=True,
			track_clicks=True,
			attachments=[{"name":"capture.jpg","type":"image/jpeg","filename":ImgFileName}]
		)


#function that will parse json and send to the right place
def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Gas Alert'

    text = MIMEText(name + ", Abnormal Gas Levels were detected. Here is an image from the sensor below: ")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    address_to_send = determine_carrier_email()

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(email, email_password)
    print(address_to_send)
    s.sendmail(email, address_to_send, msg.as_string())

    s.quit()


camera = picamera.PiCamera()

val = 0;
sensor = 0
try:
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
except:
    print("failed to connect")

a.pinMode(sensor, a.INPUT)

while True:
	val = a.analogRead(sensor)
	print(val)
	sleep(0.1)
	if val > 200:
	    camera.capture('image.jpg')
	    sleep(0.1)
	    SendSpMail('image.jpg')











