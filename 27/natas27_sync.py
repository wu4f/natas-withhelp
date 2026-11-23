import requests, time, re

CREDS = ("natas27", "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ")
URL = "http://natas27.natas.labs.overthewire.org/index.php"
POSTDATA = {'username': 'foo', 'password': 'bar'}

s = requests.Session()
r = s.post(URL, auth=CREDS, data=POSTDATA)
req = 0

while 1:
	t1 = time.time()
	r = s.post(URL, auth=CREDS, data=POSTDATA)
	if (re.search("created",r.text)):
		print(".")
		print(time.ctime(t1) + " : " + str(t1))
	else:
		print(".")
	time.sleep(1)
