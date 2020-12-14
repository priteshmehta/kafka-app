import requests
import os

def send_email(to_email, msg=None):
  if msg is None:
    msg = "Welcom to the My App! This is test email. Cheers,Pritesh"

  data = {
    "personalizations": [
      {
        "to": [
          {
            "email": to_email
          }
        ],
        "subject": "Auto-generated email From Pritesh! Have fun!"
      }
    ],
    "from": {
      "email": "priteshonmobile@gmail.com"
    },
    "content": [
      {
        "type": "text/plain",
        "value": msg
      }
    ]
  }

  api_key = os.environ.get('SENDGRID_API_KEY')
  headers = {"Authorization": "Bearer {}".format(api_key), "Content-Type": "application/json"}
  url = "https://api.sendgrid.com/v3/mail/send"

  try:
      r = requests.post(url, headers=headers, json=data)
      print(r.status_code)
      r.raise_for_status()
  except requests.exceptions.HTTPError as errh:
      print ("Http Error:", errh)
      return False
  except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:", errc)
      return False
  except requests.exceptions.Timeout as errt:
      print ("Timeout Error:", errt)
      return False
  except requests.exceptions.RequestException as err:
      print ("OOps: Something Else", err)
      return False

  return True

