from django.test import TestCase
import requests

# Create your tests here.
url = 'http://127.0.0.1:8000/api/auth/token/'

response = requests.post(url, data={'username': 'test5', 'password': 'test5'})

print(response.text)

myToken = response.json()
token = myToken['token']

header = {'Authorization': 'Token ' + token}
response = requests.get('http://127.0.0.1:8000/api/auth/user/', headers=header)

print(response.text)