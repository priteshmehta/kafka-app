from confluent_kafka import Consumer, KafkaError
import time
import random
from email_util import send_email
from sms_util import send_sms
import json
import pickle

#Cli : ./kafka/kafka_2.13-2.6.0/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group mygroup --describe
#client id : socket.gethostname()

print("### kafka Consumer ###")

def send_sms(msg_data):
	print("Sending SMS OTP to client")
	time.sleep(2)
	ret = bool(random.randint(0, 1))
	max_retry = 10
	retry_count = 0
	while not ret and retry_count < max_retry:
		time.sleep(1)
		print("Retry on failure")
		retry_count += 1
		ret = bool(random.randint(0, 1))

### Kafka Setup ####

def commit_completed():
	print("Commited successfully")

def msg_process(msg):
	msg_topic = msg.topic()
	try:
		m = pickle.loads(msg.value())
		event = json.loads(m)
		#deserialize = lambda v: json.loads(v.decode('utf-8'))
		print("Topic:", msg_topic)
		print("received event:", event)
		if msg_topic == "python_topic":
			print("Sending Email to: {}".format(event["data"]["email"]))
			email_body = "Welcom to the My App! The OTP is: {}. Cheers,Pritesh".format(event["data"]["otp"])
			if send_email(event["data"]["email"], msg=email_body):
				print("Email sent successfully")
				c.commit()
			else:
				print("Failed to send email")
		elif msg_topic == "send_sms":
			send_sms('Hi there! Pritesh is here!', event["data"]["mobile"])
			#send_sms(msg.value())
			c.commit()
	except Exception as e:
		print("Errpor:", e)

settings = {
	'bootstrap.servers': 'localhost:9092',
	'group.id': 'mygroup',
	'client.id': 'client-1',
	'enable.auto.commit': False,
	'session.timeout.ms': 6000,
	'default.topic.config': {'auto.offset.reset': 'smallest'}
	#'on_commit': commit_completed
}

c = Consumer(settings)
c.subscribe(['python_topic'])

try:
	while True:
		msg = c.poll(0.2)
		if msg is None:
			continue
		elif not msg.error():
			#print('Received message: {0}'.format(msg.value()))
			msg_process(msg)
		elif msg.error().code() == KafkaError._PARTITION_EOF:
			print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
		else:
			print('Error occured: {0}'.format(msg.error().str()))

except KeyboardInterrupt:
	pass

finally:
	c.close()
