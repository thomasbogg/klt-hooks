import requests

url = 'http://127.0.0.1:5000/'

r = requests.post(url, data='This is the data')
print(r.content)