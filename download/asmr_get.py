from email import header
import requests
import json
import time
import random

url='https://www.gscsds.org'

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.42'
}
parmas ={
    'post_id': '38741',
    'rder_id': 'null'
}
cookie = ['false']

rs = requests.post(url, headers=headers)
print(rs.cookies)