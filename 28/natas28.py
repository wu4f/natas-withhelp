#!/usr/bin/python3
import concurrent.futures
import urllib.parse
import base64
import sys
import requests
import re
import os
import binascii

url = 'http://natas28.natas.labs.overthewire.org/index.php'
executor = concurrent.futures.ThreadPoolExecutor(64)

def encrypt(s):
        r=requests.post(url,
                        auth=('natas28','JWwR438wkgTsNKBbcJoowyysdM82YjeF'),
                        params = {'query': s})
        foo = re.sub('^.*query=','',r.url)
        b64string = urllib.parse.unquote(foo)
        return base64.b64decode(b64string)

def dump(bstr):
        out_filename = 'dump.bin'
        f = open(out_filename,'wb+')
        f.write(bstr)
        f.close()
        os.system("xxd " + out_filename)
        os.system("rm " + out_filename)

def attempt(searchstr):
        print(searchstr)
        encbytes = encrypt(searchstr)
        dump(encbytes)

# Returns different block indices
def different(blocksA, blocksB):
        if(len(blocksA) != len(blocksB)):
                raise RuntimeError("Unequal input sizes")

        tagged = zip(blocksA, blocksB, range(len(blocksA)))
        unequal = filter(lambda x: x[0] != x[1], tagged)
        return list(map(lambda x: x[2], unequal))

def blocks(data):
        r = []
        while len(data) > 0:
                r.append(data[:16])
                data = data[16:]
        return r

# Figure out a prefix length that aligns the ciphertext to a block boundary
def prefix_block_align():
        base = blocks(encrypt("A" * 200))
        print("Computing block alignment...")

        for offset in range(16):
                pt = "A" * 200
                pt = pt[:64+offset] + "B" * 16 + pt[64 + (offset+16):]
                res = encrypt(pt)
                if len(different(blocks(res), base)) == 1:
                        return offset

#alignment = prefix_block_align()
alignment = 10
print("Alignment: {}".format(alignment))

def build_dict(prefix):
        result = {}

        def build_dict_entry(b):
                plaintext = prefix + bytes([b])
                ciphertext = encrypt(plaintext)[48:64]
                return (b, ciphertext, plaintext)


        print("Building dictionary...")
        for b, ciphertext, plaintext in executor.map(build_dict_entry, range(256)):
                print(plaintext, len(plaintext), binascii.hexlify(ciphertext), len(ciphertext))
                result[ciphertext] = bytes([b])

        return result

# Decrypt the input suffix one byte at a time
def decrypt():
        known_prefix = b''
        while True:
                # Compute a dictionary for all characters suffixed by the known piece
                plain = b"A" * (alignment + 15 - (len(known_prefix) % 16))
                dct = build_dict(plain + known_prefix[-(len(known_prefix) % 16):])

                # Actually find the last encrypted suffix char
                print('prefix, plain, len(plain)', known_prefix,plain,len(plain))
                actual = encrypt(plain)
                dump(actual)
                actual = actual[48+(16 * (len(known_prefix) // 16)):][:16]
                print(len(actual), actual)

                print(dct[actual])

                known_prefix += dct[actual]

decrypt()
