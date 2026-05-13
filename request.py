#import requests
#import json
#from settings import SECRET_KEY
#
#url = 'https://klt-hooks.up.railway.app/webhook'
#
#headers = {
#    "Authorization": f"Bearer {SECRET_KEY}"
#}
#
#r = requests.post(url, data=json.dumps({"message": "This is the data"}), headers=headers)
#print(r.content)
#
import requests
import json

url = "https://sandbox-merchant.revolut.com/api/webhooks"

payload = json.dumps({
  "url": "https://example.com/webhooks",
  "events": [
    "ORDER_COMPLETED",
    "ORDER_AUTHORISED"
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer <yourSecretApiKey>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)