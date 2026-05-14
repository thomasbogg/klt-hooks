import json
import requests
from settings import REVOLUT_API_VERSION, REVOLUT_SECRET_KEY, KLT_SECRET_KEY

def send_test_request():
  
  url = 'https://klt-hooks.up.railway.app/test'
  
  headers = {
      "Authorization": f"Bearer {KLT_SECRET_KEY}"
  }
  
  response = requests.post(url, data=json.dumps({"message": "This is the data"}), headers=headers)
  print(response.content)
  print(response.status_code)
  print(response.text)
  


def create_revolut_webhook():
  url = "https://sandbox-merchant.revolut.com/api/webhooks"

  payload = {
    "url": "https://klt-hooks.up.railway.app/revolutcallback",
    "events": [
      "ORDER_COMPLETED",
      "ORDER_AUTHORISED"
    ]
  }
  post_request(url, payload, REVOLUT_SECRET_KEY)


def create_revolut_payment_order(description = None, full_name = None, email = None, phone = None, amount = 2400):
  url = "https://sandbox-merchant.revolut.com/api/orders"
  
  payload = ({
    'amount': amount,
    'currency': 'EUR',
    'description': 'Test payment',
    'customer': {
      'email': 'thomasbogg@gmail.com',
      'phone': '+351 935 769 935',
      'full_name': 'Thomas Bogg'
    },
  })
  post_request(url, payload, REVOLUT_SECRET_KEY)


def generate_request_headers(secret_key = None):
  return {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {secret_key}',
    'Revolut-Api-Version': REVOLUT_API_VERSION,
  }


def post_request(url, data, secret_key):
  headers = generate_request_headers(secret_key)
  response = requests.request("POST", url, headers=headers, json=data)
  print(response.text)


if __name__ == "__main__":
  create_revolut_payment_order()