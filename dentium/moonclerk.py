import requests
import csv
import json

with open('auth.txt') as f:
    api_cred = f.readlines()[0]

urls = [('forms', 'https://api.moonclerk.com/forms'),
        ('payments', 'https://api.moonclerk.com/payments'),
        ('customers', 'https://api.moonclerk.com/customers')]

headers = {
    "Authorization": "Token token={}".format(api_cred),
    "Accept": "application/vnd.moonclerk+json;version=1"
}

hit_api = lambda t: requests.get(t[1], headers=headers).json()[t[0]]
data = [hit_api(x) for x in urls]

