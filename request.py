import requests
import json
from settings import SECRET_KEY

url = 'https://klt-hooks.up.railway.app/webhook'

headers = {
    "Authorization": f"Bearer {SECRET_KEY}"
}

r = requests.post(url, data=json.dumps({"message": "This is the data"}), headers=headers)
print(r.content)