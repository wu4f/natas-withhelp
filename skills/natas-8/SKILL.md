---
name: natas-8
description: >-
  Use when solving OverTheWire natas8: given natas8 credentials, reverse the
  bin2hex(strrev(base64_encode)) transform on the leaked encodedSecret, POST the
  plaintext secret, and extract the natas9 password.
---
# natas8

**Input:** username and password for natas8.

**Weakness:** the source exposes `$encodedSecret` and `encodeSecret()` = `bin2hex(strrev(base64_encode($secret)))`. Reverse that transform offline, then POST the plaintext secret.

**Network:** run on a host that can reach `natas8.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Fetch the viewable source and note `$encodedSecret`:

```bash
curl.exe -s -u USER:PASS http://natas8.natas.labs.overthewire.org/index-source.html
```

2. Derive the natas9 password (never hardcode the secret or password). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, html as htmlmod, re, sys, urllib.parse, urllib.request
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
base = "http://natas8.natas.labs.overthewire.org"
def get(path):
    req = urllib.request.Request(base + path, headers={"Authorization": auth})
    return urllib.request.urlopen(req, timeout=30).read().decode()
src = get("/index-source.html")
plain = htmlmod.unescape(re.sub(r"<[^>]+>", "", src))
m = re.search(r'\$encodedSecret\s*=\s*"([0-9a-fA-F]+)"', plain)
secret = base64.b64decode(bytes.fromhex(m.group(1))[::-1]).decode()
data = urllib.parse.urlencode({"secret": secret, "submit": "1"}).encode()
req = urllib.request.Request(base + "/", data=data, headers={"Authorization": auth})
body = urllib.request.urlopen(req, timeout=30).read().decode()
print(re.search(r"password for natas9 is ([A-Za-z0-9]+)", body).group(1))
```

3. The printed string is the natas9 password.

4. Confirm by GETting `http://natas9.natas.labs.overthewire.org/` with Basic Auth `natas9:<password>` and expecting HTTP 200.
