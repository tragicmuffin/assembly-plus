#!/usr/bin/python3

## Launches the interpreter for an A+ program
## Can be used in a terminal, or on the web using CGI
## Inputs: (A+ source, CGI flag)

import sys
sys.path.insert(0, "lib")  # add lib folder as import location
import aplus2py as a2p
import json
import cgi

# Assume CGI by default. Turn off when -nocgi is passed in command line argument.
use_cgi = True
try:
	if "-nocgi" in sys.argv[1:]:
		use_cgi = False
except:
	pass

### Web only ###
if(use_cgi):
	fs = cgi.FieldStorage()

	# Get JSON input. d['stdin'] will hold the input code.
	d = {}
	for k in fs.keys():
	    d[k] = fs.getvalue(k)

	print ("Content-Type: application/html")
	print ("")
################
else:
	print("")


lines = []	# a list to store all lines of program
linenum = 0

error = False
print("<== Interpreter starting. ==>\n")

try:
	if(use_cgi):
		src = d['stdin']  # run code from JSON input
	else:
		src = open('Examples\\fibonacci.aplus', 'r')  # run from file

except:
	print("<== Error: Cannot read file. ==>")
	print("\n<== Interpreter stopped. ==>\n")
	error = True


### Web only ###
if(use_cgi):
	# Read input from JSON
	# Separate lines into list
	lines = src.split('\n')
################
else:
	# Read from file
	# Dump all lines of program into a list
	line = src.readline()
	while line != '':
		lines.append(line)
		line = src.readline()
	src.close()

# Iterate through lines in list for parsing
while not error:
	if linenum >= len(lines):
		break  # end of source file

	if lines[linenum] == '\n':
		linenum += 1
		continue  # blank line, so skip it

	code = a2p.parseLine(lines, linenum)

	# If a value >0 was returned, this was a loop and we will update the linenum to the returned counter.
	if code > 0:
		linenum = code

	linenum += 1  # keep track of line number

	# A 0 will be returned from parseLine unless an error occurs, in which case a -1 is returned.
	if code == -1:
		print("\n<== Interpreter stopped. ==>\n")
		error = True
		break

# Loop finished
if not error:
	print("\n<== Program finished successfully. ==>\n")
