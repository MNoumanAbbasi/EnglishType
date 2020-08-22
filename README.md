# EnglishType

A YAPL built using Python for course CS315: Theory of Automata final project.

## [Table of contents](#table-of-contents)
* [Requirements](#requirements)
* [Introduction](#introduction)
* [Getting Started](#getting-started)
  * [Running a file](#running-a-file)
  * [Examples](#examples)
* [Syntax](#syntax)
  * [Declaring a variable](#declaring-a-variable)
  * [Assigning a variable](#assigning-a-variable)
  * [Printing](#printing)
  * [Conditional statements](#conditional-statements)
  * [Lists](#lists)

## Requirements

- PLY library [here](https://github.com/dabeaz/ply)
- Python 3.6 and above

## Introduction

EnglishType is a simple programming language built upon Python and uses the PLY library for parsing tools lex and yacc.
  
The syntax is designed in a way to make it as similar to casual English language as possible while not compromising on the funtionality of a basic programming language. This ensures the language is easy to understand and to get started.

## Getting Started

- Fulfill the requirements.
- Clone the repo
  - Or download parser.py, lexer.py and interpreter.py (you only need these)
- Run the command:  `python3 interpreter.py`
- Type `PRINT 1 + 2;` in the command line interpreter environment

Note: The command line interpreter does not yet support multiline statements.

### Running a file

Run the command and replace filename with the required name of file to interpret:

```shell
python3 interpreter.py [filename]
```

### Examples

Examples test files can be found in the folder test_cases. Use it to understand the syntax

## Syntax

Keywords are always uppercase and every statement must end with a semi-colon ';'. (I may change this to a period '.' in the future to make it more similar to English language).

### Declaring a variable

```
DECLARE INT i;
DECLARE INT j TO 5;
DECLARE STRING myString TO "Hello World!";
```

Supports all basic primitive types. Uninitalized variables will be set to NoneType of Python.

### Assigning a variable

```
SET i TO 10;
```

### Printing

```
PRINT i;
PRINT myString;
```

Output:
```
10
Hello World!
```

### Conditional statements

```
DECLARE BOOL isRaining TO True;
DECLARE BOOL isSnowing TO False;
DECLARE BOOL temp TO 0;
IF (isRaining EQUALS True)
{
    IF(temp > 45) {
        PRINT "Wear lightweight raincoat";
    }
    ELSEIF(temp EQUALS 45) {
        PRINT "Wear lightweight raincoat";
    }
    ELSE {
        PRINT "Wear fleece and raincoat";
    }
}
ELSEIF (isSnowing NOTEQUALS False)
{
    PRINT "Wear soft shell jacket";
}
ELSE {
    PRINT "It is hard to come up with interesting examples";
}
```

Output:
```
Wear fleece and raincoat
```

### Lists

Lists can have elements of varying data types (similar to Python).

```
DECLARE LIST myList TO [1,2,3,4,5,6];
PRINT myList SLICE 0, 2;
myList PUSH 7;
PRINT myList AT 3;
```

Output:
```
[1, 2]
4
```

### And more

Read the examples given in the folder test_cases for more in-depth examples.
