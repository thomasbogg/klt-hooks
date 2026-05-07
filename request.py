import requests

url = 'https://klt-hooks.up.railway.app/webhook'

r = requests.post(url, data='This is the data')
print(r.content)