---
name: natas-11
description: >-
  Use when solving OverTheWire natas11: given natas11 credentials, recover the
  repeating XOR key from the default data cookie (known plaintext is the default
  JSON), forge a cookie with showpassword=yes, and extract the natas12 password.
---
# natas11

**Input:** username and password for natas11.

**Weakness:** the `data` cookie is `base64(xor_encrypt(json_encode(array), key))` with a short repeating key. The default array is known plaintext (`{"showpassword":"no","bgcolor":"#ffffff"}`), so XOR the known JSON against the server's default cookie to recover the key, then forge a cookie with `showpassword` set to `yes`.

**Network:** run on a host that can reach `natas11.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. Derive the natas12 password (never hardcode it). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, json, re, sys, urllib.parse, urllib.request
from http.cookiejar import CookieJar
BASE = "http://natas11.natas.labs.overthewire.org"
def xor(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
resp = opener.open(urllib.request.Request(BASE + "/", headers={"Authorization": auth}), timeout=30)
cipher = base64.b64decode(urllib.parse.unquote(re.search(r"data=([^;]+)", resp.headers.get("Set-Cookie", "")).group(1)))
known = json.dumps({"showpassword": "no", "bgcolor": "#ffffff"}, separators=(",", ":")).encode()
full = xor(known, cipher)
key = next(full[:k] for k in range(1, len(full) + 1) if all(full[i] == full[i % k] for i in range(len(full))))
plain = json.dumps({"showpassword": "yes", "bgcolor": "#ffffff"}, separators=(",", ":")).encode()
forged = base64.b64encode(xor(plain, key)).decode()
req = urllib.request.Request(BASE + "/", headers={"Authorization": auth, "Cookie": "data=" + urllib.parse.quote(forged)})
html = urllib.request.urlopen(req, timeout=30).read().decode()
print(re.search(r"password for natas12 is ([A-Za-z0-9]{32})", html).group(1))
```

2. The printed string is the natas12 password.

3. Confirm by GETting `http://natas12.natas.labs.overthewire.org/` with Basic Auth `natas12:<password>` and expecting HTTP 200.

**Note:** the known plaintext must match PHP's `json_encode` output exactly (no spaces, forward slashes only matter if present). If the default array ever changes, update `known` to match the current default cookie.
