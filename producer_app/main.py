from confluent_kafka import Producer
import uuid
import random
import json
import pickle

### cli
# ./kafka_2.13-2.6.0/bin/kafka-topics.sh --zookeeper=127.0.0.1:2181 --list
# ./kafka_2.13-2.6.0/bin/kafka-topics.sh --zookeeper=127.0.0.1:2181 --topic first_topic --create --partitions 3 --replication-factor 1
############################################

settings = {
	'bootstrap.servers': 'localhost:9092'
}

def publish_message(message, email=None):
	msg = get_msg(message, email)
	p = Producer(settings)
	p.produce('python_topic', key=msg["key"], value=msg["data"], callback=acked)
	p.flush(30)

def get_msg(text_msg, email):
	msg_id = str(uuid.uuid1())
	msg_key = random.randint(0, 10)
	if email is None:
		email = "mehtapritesh+{}@gmail.com".format(random.randint(0, 100))
	otp = ""
	for i in range(1, 5):
		otp += str(random.randint(0, 9))
	kafka_msg = {
		"id": msg_id,
		"key": str(msg_key),
		"data": {"text": text_msg, "otp": otp, "email": email, "mobile": "+9112121212"}
	}
	print("Kafka Message: {}".format(kafka_msg))
	m = json.dumps(kafka_msg)
	return {"key": str(msg_key), "data": pickle.dumps(m)}

def acked(err, msg):
	if err:
		print("Failed to delivery message. {} {}".format(msg.value(), err.str()))
	else:
		print("Message delivered successfully")

publish_message("This is webapp message")

#print(" #### Sample Kafka Producer ###")
# for i in range(1, 3):
# 	msg = get_msg("test message{}".format(i))
# 	p = Producer(settings)
# 	p.produce('python_topic', key=msg["key"], value=msg["data"], callback=acked)
# 	p.poll(0.5)

# p.flush(30)

