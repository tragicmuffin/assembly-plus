## A+ to Python interpreter
 # Input: .aplus source file
 # Output: python program output

vars = {}	# a dict to hold all variables created by program
cons = {}	# a dict to hold all constants created by program
types = {}	# a dict to hold types for each variable/constant

def throwError(msg, lnum):
	print("Compiler Error: " + msg + " Line #" + str(lnum))

def handleKeyword(keyword, args, lnum):
	### `var` ###
	if keyword == "var":
		# args[0] will be variable type / args[1] will be variable name

		if args[1] in vars:
			throwError("Variable named '"+ args[0] +"' already exists. Try `set` instead.", lnum)
		elif args[1] in cons:
			throwError("Constant named '"+ args[0] +"' already exists.", lnum)
		elif not args[1][0].isalpha():
			throwError("Variable names must begin with a letter.", lnum)
		else:
			if args[0] == "bool":
				vars[args[1]] = False  # "declare" a variable with the given name and initialize it to false.
				types[args[1]] = "bool"
			elif args[0] == "uint8":
				vars[args[1]] = 0  # "declare" a variable with the given name and initialize it to 0.
				types[args[1]] = "uint8"
			elif args[0] == "string":
				vars[args[1]] = ''  # "declare" a variable with the given name and initialize it to ''.
				types[args[1]] = "string"
			else:
				throwError("Unrecognized type `"+ args[0] +"`.", lnum)

	### `set` ###
	elif keyword == "set":
		# args[0] will be variable name / args[1] will be assignment operator / args[2] will be variable value
		if (len(args) != 3):
			throwError("Incorrect number of arguments to `set` keyword.", lnum)
		elif args[0] not in vars:
			throwError("No variable named '"+ args[0] +"' exists. Try declaring one first with `var`.", lnum)
		elif args[1] not in ["=", "+=", "-="]:
			throwError("Unrecognized assignment operator `"+ args[1] +"`.", lnum)
		else:
			if types[args[0]] == "uint8":
				try:
					val = int(args[2])
				except:
					throwError("Invalid value '"+ args[2] +"' for type `"+ types[args[0]] +"`.", lnum)

				if val not in range(0,256):
					throwError("Invalid value '"+ args[2] +"' for type `"+ types[args[0]] +"`.", lnum)

				elif args[1] == "=":
					vars[args[0]] = int(args[2])
				elif args[1] == "+=":
					vars[args[0]] += int(args[2])
				elif args[1] == "-=":
					vars[args[0]] -= int(args[2])

			elif types[args[0]] == "bool":
				if args[1] == "=":
					if args[2] == 'true':
						vars[args[0]] = True
					elif args[2] == 'false':
						vars[args[0]] = False
					else:
						throwError("Invalid value '"+ args[2] +"' for type `"+ types[args[0]] +"`.", lnum)
				else:
					throwError("Assignment operator `"+ args[1] +"` is not valid for type `"+ types[args[0]] +"`.", lnum)

			elif types[args[0]] == "string":
				var_str = ' '.join(args[2:])  # rejoin string following 'print' command
				if args[1] == "=":
					if (var_str[0] != '"' || var_str[-1] != '"')
						throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
					else:
						vars[args[0]] = var_str.strip('"')
						types[args[0]] = "string"

				if args[1] == "+=":
					if (var_str[0] != '"' || var_str[-1] != '"')
						throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
					else:
						vars[args[0]] += var_str.strip('"')
						types[args[0]] = "string"

				else:
					throwError("Assignment operator `"+ args[1] +"` is not valid for type `"+ types[args[0]] +"`.", lnum)

	### `con` ###
	elif keyword == "con":
		# args[0] will be constant type / args[1] will be constant name
		# args[2] will be assignment operator / args[3] will be constant value
		if (len(args) != 4):
			throwError("Incorrect number of arguments to `con` keyword.", lnum)
		elif args[1] in cons:
			throwError("Constant named '"+ args[1] +"' already exists.", lnum)
		elif not args[1][0].isalpha():
			throwError("Constant names must begin with a letter.", lnum)
		elif args[2] not in ["="]:
			throwError("Unrecognized assignment operator `"+ args[2] +"`.", lnum)
		else:
			if args[0] == "bool":
				if args[3] == 'false':
					cons[args[1]] = False
					types[args[1]] = "bool"
				elif args[3] == 'true':
					cons[args[1]] = True
					types[args[1]] = "bool"
				else:
					throwError("Invalid value '"+ args[3] +"' for type `"+ args[0] +"`.", lnum)
			elif args[0] == "uint8":
				if int(args[3]) in range(0,256):
					cons[args[1]] = int(args[3])
					types[args[1]] = "uint8"
				else:
					throwError("Invalid value '"+ args[3] +"' for type `"+ args[0] +"`.", lnum)
			elif args[0] == "string":
				var_str = ' '.join(args[3:])  # rejoin string following 'print' command
				if (var_str[0] != '"' || var_str[-1] != '"')
					throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
				else:
					cons[args[1]] = var_str.strip('"')
					types[args[1]] = "string"
			else:
				throwError("Unrecognized type `"+ args[0] +"`.", lnum)


	### `print` ###
	elif keyword == "print":

		toprint = ' '.join(args)  # rejoin string following 'print' command
		if (toprint[0] != '"' || toprint[-1] != '"')
			# check if provided string starts and ends with quotation marks
			throwError("String provided to `print` function is not properly formatted. Strings must start and end with double quotation marks.", lnum)
		else:
			print(args[0].strip('"'))  # print the string that comes after 'print' command, stripping off any quotes

	else:
		throwError("Unrecognized keyword `"+ keyword +"`.", lnum)

def parseLine(l, lnum):
	# Used to parse a single line of A+ code. Returns the line
	l = l.strip()  # remove newline characters and trailing/leading whitespace

	# Read the last character in the line.
	if (l[-1] == ';'):
		# This is a basic statement
		l = l[:-1]  # remove semicolon
		tokens = l.split() # make a list of words in the line
		handleKeyword(tokens[0], tokens[1:], lnum) # pass keywords and arguments to handler

	elif (l[-1] == ':'):
		# This is a conditional (if/while) statement
		l = l[:-1]  # remove colon
	else:
		# This is an unrecognized statements
		pass

if __name__ == __main__:
	srcin = open('helloworld.aplus', 'r')
	srcout = open('helloworld.py', 'w')
	linenum = 0

	while True:
		linenum += 1  # keep track of line number
		line = srcin.readline()
		parseLine(line, linenum)
