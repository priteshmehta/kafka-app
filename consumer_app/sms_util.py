#ACb0832397b5d07ea79854f6d80596c465
#Token: 82e24f6eddc47d6461ac88c1cc8bbb63

import os
from twilio.rest import Client


def send_sms(msg, receiver):
	account_sid = os.environ['TWILIO_ACCOUNT_SID']
	auth_token = os.environ['TWILIO_AUTH_TOKEN']
	client = Client(account_sid, auth_token)
	message = client.messages.create(body=msg, from_='Skrilla', to=receiver)
	print(message.sid)


#send_sms('Hi there! Pritesh is here!', '+919765895056')