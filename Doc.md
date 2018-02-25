# Documentation for the A+ language

## 1. Data Types
| Name	    | Size		| Purpose		        	 | Range 	           |
|:---------:|:---------:| -------------------------- | ------------------- |
| bool    	| 1 byte    | Boolean			         | `true` or `false`   |
| uint8    	| 1 byte	| 8-bit unsigned integer     | 0 - 255        	   |
| string    | n bytes   | String of ASCII characters | N/A                 |


## 2. Syntax

### Basics
All statements must be ended with a semicolon.

Comments must be wrapped in /\* and \*/.  
Example: `/* This is a comment. */`

----
### Keywords
| Keyword   | Purpose		        			    | Example 	              |
|:---------:| ------------------------------------- | ----------------------- |
| var     	| Declares a mutable variable.          | `var uint8 foo;`        |
| con	    | Creates a constant.                  	| `con uint8 BAR = 23;`   |
| print	   	| Prints a line to stdout.           	| `print "Hello, world!";`|

### `var`
Use `var uint8 foo;` to declare a uint8 variable named foo. The `var` keyword must always be followed by the variable type. Variables must be declared before they are assigned.

### `con`
Use `con uint8 BAR = 23;` to create a constant. The `con` keyword must always be followed by the variable type. Constants must be set when they are declared.

### `print`
Use `print "Hello, World!";` to print a string to stdout followed by a new line. `print` can print any data type, but will print the ASCII equivalent characters for each byte.

----
### Control Flow

#### `if`
The condition of the if statement must be wrapped in parentheses ( ) and the conditional block must be wrapped in braces { }.  
Example:  
```
if(foo == 1) {
    /* Do something */
}
```

#### `while`
The condition of the while statement must be wrapped in parentheses ( ) and the conditional block must be wrapped in braces { }.  
Example:  
```
var uint8 foo;
foo = 0;
while(foo < 10) {
    /* Do something */
    foo = foo + 1;
}
```

----
### Operators
| Operator	| Type		| Purpose                   | Example 		|
|:---------:| --------- | ------------------------- | ------------- |
| +		    | Binary	| Adds two numbers.		    | `a + b`	    |
| -		    | Binary	| Subtracts two numbers.	| `a - b` 	    |
| \*	    | Binary	| Multiplies two numbers.	| `a * b`  	    |
| /	    	| Binary	| Divides two numbers.		| `a / b`  	    |


## 3. ????
