## A+ to Python interpreter
 # Input: .aplus source file
 # Output: python program output

vars = {}	# a dict to hold all variables created by program
cons = {}	# a dict to hold all constants created by program
types = {}	# a dict to hold types for each variable/constant

def throwError(msg, lnum):
	print("<== Error: " + msg + " Line #" + str(lnum+1) + " ==>")
	return -1

def handleKeyword(keyword, args, lnum):
	### `var` ###
	if keyword == "var":
		# args[0] will be variable type / args[1] will be variable name
		if (len(args) != 2):
			return throwError("Incorrect number of arguments to `var` keyword.", lnum)
		elif args[1] in vars:
			return throwError("Variable named '"+ args[0] +"' already exists. Try `set` instead.", lnum)
		elif args[1] in cons:
			return throwError("Constant named '"+ args[0] +"' already exists.", lnum)
		elif not args[1][0].isalpha():
			return throwError("Variable names must begin with a letter.", lnum)
		else:
			if args[0] == "bool":
				vars[args[1]] = False  		# "declare" a variable with the given name and initialize it to false.
				types[args[1]] = "bool"
			elif args[0] == "uint8":
				vars[args[1]] = 0  			# "declare" a variable with the given name and initialize it to 0.
				types[args[1]] = "uint8"
			elif args[0] == "int":
				vars[args[1]] = 0  			# "declare" a variable with the given name and initialize it to 0.
				types[args[1]] = "int"
			elif args[0] == "string":
				vars[args[1]] = ''  		# "declare" a variable with the given name and initialize it to ''.
				types[args[1]] = "string"
			else:
				return throwError("Unrecognized type `"+ args[0] +"`.", lnum)

	### `set` ###
	elif keyword == "set":
		# args[0] will be variable name / args[1] will be assignment operator / args[2+] will be variable value

		## Evaluate expression ##
		if (len(args) == 3):
			# Only one argument in expression. Check if it's a variable name or literal.
			exp = args[2]
			if (exp[0].isalpha() and exp not in ['true', 'false']):
				# If the expression starts with an alpha character but it isn't a bool keyword, then it's a variable.
				if exp in vars:
					exp = vars[exp]  # pull value from variable
				elif exp in cons:
					exp = cons[exp]  # pull value from constant
				else:
					return throwError("No variable or constant named '"+ args[2] +"' exists.", lnum)
			# Otherwise, it must be a literal, so pass it along as-is.

		elif (len(args) == 5):
			# Three arguments in expression.
			expL = args[2]
			opr = args[3]
			expR = args[4]

			if opr not in ['+', '-', '*', '/']:
				return throwError("Invalid operator '"+ opr +"'.", lnum)
			else:
				if (expL[0].isalpha() and expL not in ['true', 'false']):
					# If the left side starts with an alpha character but it isn't a bool keyword, then it's a variable.
					if expL in vars:
						expL = vars[expL]  # pull value from variable
					elif expL in cons:
						expL = cons[expL]  # pull value from constant
					else:
						return throwError("No variable or constant named '"+ expL +"' exists.", lnum)
				if (expR[0].isalpha() and expR not in ['true', 'false']):
					# If the right side starts with an alpha character but it isn't a bool keyword, then it's a variable.
					if expR in vars:
						expR = vars[expR]  # pull value from variable
					elif expR in cons:
						expR = cons[expR]  # pull value from constant
					else:
						return throwError("No variable or constant named '"+ expR +"' exists.", lnum)
				# If either expL or expR is a literal, it will be passed along as-is
				if opr == '+':
					exp = int(expL) + int(expR)
				elif opr == '-':
					exp = int(expL) - int(expR)
				elif opr == '*':
					exp = int(expL) * int(expR)
				elif opr == '/':
					exp = int(expL) / int(expR)
		else:
			return throwError("Incorrect number of arguments to `set` keyword.", lnum)

		## Set variable ##
		if args[0] in cons:
			return throwError("Attempt to change value of constant '"+ args[0] +"'.", lnum)
		elif args[0] not in vars:
			return throwError("No variable named '"+ args[0] +"' exists. Try declaring one first with `var`.", lnum)
		elif args[1] not in ["=", "+=", "-="]:
			return throwError("Unrecognized assignment operator `"+ args[1] +"`.", lnum)
		else:
			if types[args[0]] == "uint8" or types[args[0]] == "int":
				try:
					val = int(exp)
				except:
					return throwError("Invalid value '"+ str(exp) +"' for type `"+ types[args[0]] +"`.", lnum)

				if (types[args[0]] == "uint8" and val not in range(0,256)):
					return throwError("Value '"+ str(exp) +"' out of bounds for type `"+ types[args[0]] +"`.", lnum)

				elif args[1] == "=":
					vars[args[0]] = int(exp)
				elif args[1] == "+=":
					vars[args[0]] += int(exp)
				elif args[1] == "-=":
					vars[args[0]] -= int(exp)

			elif types[args[0]] == "bool":
				if args[1] == "=":
					if exp == 'true':
						vars[args[0]] = True
					elif exp == 'false':
						vars[args[0]] = False
					else:
						return throwError("Invalid value '"+ str(exp) +"' for type `"+ types[args[0]] +"`.", lnum)
				else:
					return throwError("Assignment operator `"+ args[1] +"` is not valid for type `"+ types[args[0]] +"`.", lnum)

			elif types[args[0]] == "string":
				var_str = ' '.join(args[2:])  # rejoin string following 'print' command
				if args[1] == "=":
					if (var_str[0] != '"' or var_str[-1] != '"'):
						return throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
					else:
						vars[args[0]] = var_str.strip('"')
						types[args[0]] = "string"

				if args[1] == "+=":
					if (var_str[0] != '"' or var_str[-1] != '"'):
						return throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
					else:
						vars[args[0]] += var_str.strip('"')
						types[args[0]] = "string"

				else:
					return throwError("Assignment operator `"+ args[1] +"` is not valid for type `"+ types[args[0]] +"`.", lnum)

	### `con` ###
	elif keyword == "con":
		# args[0] will be constant type / args[1] will be constant name
		# args[2] will be assignment operator / args[3] will be constant value
		if (len(args) != 4):
			return throwError("Incorrect number of arguments to `con` keyword.", lnum)
		elif args[1] in cons:
			return throwError("Constant named '"+ args[1] +"' already exists.", lnum)
		elif not args[1][0].isalpha():
			return throwError("Constant names must begin with a letter.", lnum)
		elif args[2] not in ["="]:
			return throwError("Unrecognized assignment operator `"+ args[2] +"`.", lnum)
		else:
			if args[0] == "bool":
				if args[3] == 'false':
					cons[args[1]] = False
					types[args[1]] = "bool"
				elif args[3] == 'true':
					cons[args[1]] = True
					types[args[1]] = "bool"
				else:
					return throwError("Invalid value '"+ args[3] +"' for type `"+ args[0] +"`.", lnum)

			elif args[0] == "uint8":
				if int(args[3]) in range(0,256):
					cons[args[1]] = int(args[3])
					types[args[1]] = "uint8"
				else:
					return throwError("Value '"+ args[3] +"' out of bounds for type `"+ args[0] +"`.", lnum)

			elif args[0] == "int":
				try:
					cons[args[1]] = int(args[3])
				except:
					return throwError("Invalid value '"+ args[3] +"' for type `"+ args[0] +"`.", lnum)
				types[args[1]] = "int"

			elif args[0] == "string":
				var_str = ' '.join(args[3:])  # rejoin string following 'print' command
				if (var_str[0] != '"' or var_str[-1] != '"'):
					return throwError("String is not properly formatted. Strings must start and end with double quotation marks.", lnum)
				else:
					cons[args[1]] = var_str.strip('"')
					types[args[1]] = "string"
			else:
				return throwError("Unrecognized type `"+ args[0] +"`.", lnum)


	### `print` ###
	elif keyword == "print":

		toprint = ' '.join(args)  # rejoin string following 'print' command

		if toprint[0] != '"':
			# Assume it is a variable/constant name
			if toprint in vars:
				toprint = vars[toprint]  # pull value from variable
			elif toprint in cons:
				toprint = cons[toprint]  # pull value from constant
			else:
				return throwError("No variable or constant named '"+ toprint +"' exists.", lnum)
		elif (toprint[-1] != '"'):
			# Check if provided string ends with quotation marks
			return throwError("String provided to `print` function is not properly formatted. Strings must start and end with double quotation marks.", lnum)

		print(str(toprint).strip('"'))  # print the string that comes after 'print' command, stripping off any quotes

	else:
		return throwError("Unrecognized keyword `"+ keyword +"`.", lnum)

	return 0

def handleLoop(cond, lnum, lines):
	if (cond[0].isalpha() and cond not in ['true', 'false']):
		# Make sure variable/constant is an integer. If so, fetch variable/constant value.
		if cond in types:
			if types[cond] == 'int' or types[cond] == 'uint8':
				if cond in vars:
					iters = vars[cond]
				else:
					iters = cons[cond]
			else:
				return throwError("Invalid type `"+ types[cond] +"` for `loop` condition. Must be an integer type.", lnum)
		else:
			return throwError("No variable or constant named '"+ cond +"' exists.", lnum)
	else:
		# Literal number of iterations. Check if the number is valid.
		if not cond.isdecimal():
			return throwError("Literal value '"+ cond +"' in `loop` condition must be an integer.", lnum)
		elif int(cond) < 1:
			return throwError("Literal value '"+ cond +"' in `loop` condition must be a positive integer.", lnum)
		else:
			iters = int(cond)

	# Line 1: Expect a '{' here
	lnum += 1
	line = lines[lnum]
	if line.strip() != '{':
		return throwError("Expected '{'.", lnum)

	# Line 2+
	start_lnum = lnum  # save starting line number before looping

	for i in range(iters):
		lnum += 1

		while lines[lnum].strip() != '}':
			parseLine(lines, lnum)
			lnum += 1
			try:
				lines[lnum]
			except IndexError:
				return throwError("Reached end of file. Expected '}' to end loop.", lnum)
			except:
				return throwError("Expected '}' to end loop.", lnum)
		if i < iters-1:
			lnum = start_lnum  # reset line number for next iteration (unless we are on last iteration)

	return lnum  # return last line number so global line counter can be updated

def parseLine(lines, lnum):
	# Used to parse a single line of A+ code. Returns the line
	l = lines[lnum].strip()  # remove newline characters and trailing/leading whitespace

	# Read the last character in the line.
	if (l[-1] == ';'):
		# This is a basic statement
		l = l[:-1]  # remove semicolon
		tokens = l.split() # make a list of words in the line
		try:
			return handleKeyword(tokens[0], tokens[1:], lnum) # pass keywords and arguments to handler
		except:
			throwError("Cannot read line.", lnum)
			return -1


	elif (l[-1] == ':'):
		# This is a conditional (if/while) statement
		l = l[:-1]  # remove colon
		# Determine which control statement we have
		ctrl = l[:l.find('(')]
		if ctrl not in ['loop', 'while', 'if']:
			throwError
		else:
			condition = l[l.find('(')+1 : l.find(')')]
			if ctrl == 'loop':
				return handleLoop(condition, lnum, lines)
			elif ctrl == 'while':
				return handleWhile(condition, lnum, lines)
			elif ctrl == 'if':
				return handleIf(condition, lnum, lines)


	elif (l[:2] == '/*'):
		# This should be a comment
		if (l[-2:] == '*/'):
			pass
		else:
			return throwError("Improper comment syntax. Comments must end with '*/'.", lnum)

	else:
		# This is an unrecognized statement
		return throwError("Unrecognized statement. Expected ';' or ':'.", lnum)

	return 0



if __name__ == "__main__":
	lines = []	# a list to store all lines of program
	linenum = 0

	error = False
	print("\n<== Interpreter starting. ==>")

	try:
		src = open('Examples\\fibonacci.aplus', 'r')
	except:
		print("<== Error: Cannot read file. ==>")
		print("<== Interpreter stopped. ==>\n")
		error = True

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

		code = parseLine(lines[linenum], linenum)

		linenum += 1  # keep track of line number

		# A 0 will be returned from parseLine unless an error occurs, in which case a 1 is returned.
		if code == 1:
			print("<== Interpreter stopped. ==>\n")
			error = True
			break

	# Loop finished
	if not error:
		print("<== Program finished successfully. ==>")
