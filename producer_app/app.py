from flask import Flask, request
from main import publish_message

app = Flask(__name__)

#http://127.0.0.1:5000/send?email=mehta.pritesh@gmail.com&message=hello world!

@app.route('/')
def hello():
	return "Sample web app to send email"

@app.route('/send', methods=['POST'])
def send_email():
	#req_data = request.get_json()
	msg = request.args.get('language')
	email = request.args.get('email')
	try:
		publish_message(msg, email)
		return {"status": 200}
	except Exception as e:
		return {"status": 500, "error": e}

if __name__ == '__main__':
	app.run(port=5000)