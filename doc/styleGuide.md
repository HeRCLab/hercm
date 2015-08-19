# HeRCM coding style guide 
This document explains the stylistic choices used in the project, to ensure maximum readability and maintainability. None of these are hard and fast rules though, as working code is better than no code! Updating existing code to the style guide is considered low priority, but would be a good way for a beginner to start contributing. 

# Naming conventions 
Names should always be as descriptive as possible, even if that makes them long. The only exception to this is iterators. Acceptable names for iterators are `i`, `j`, or `k`. Names used to interfaces with foreign APIs may violate naming conventions in order to maintain consistency with that API's naming conventions, at the discretion of the author. 

Names should always be camelCased. Here are some examples:

## Preferred 
* `variableName`
* `longVariableName` 
## Acceptable 
* `VariableName`
* `LongVariableName`
## Unacceptable 
* `variable_name`
* `long_variableName`

Additionally, class instances may be in all caps rather than camelCased, at the discretion of the code author. 

# Line length
All code files should strictly adhere to a maximum line length of 80 characters. Documentation files do not need to adhere to any particular line length. Only in the case where required functionality would otherwise be impossible may any line of code exceed 80 characters. 

As many function names are long, and have many arguments, it is acceptable to split arguments over several lines. Examples: 

## Preferred 
```
myReallLongFunctionCall(longArgumentOne, 
	longArgumentTwo, 
	longArgumentThree,
	"{1},{2}".format(VariableWithLongName, 
		OtherVariableWithLongName),
	longArgumentFour)
```

## Acceptable 
```
myReallLongFunctionCall(longArgumentOne, 
						longArgumentTwo, 
						longArgumentThree,
						"{1},{2}".format(VariableWithLongName, 
										 OtherVariableWithLongName),
						longArgumentFour)
```

## Unacceptable 
```
myReallLongFunctionCall(longArgumentOne, longArgumentTwo, longArgumentThree,"{1},{2}".format(VariableWithLongName, OtherVariableWithLongName),longArgumentFour)
```

# Comments
All functions (including class constructions), should include comments explaining the function's purpose, arguments, return values, and exceptions (if any). Code which is nontrivial or non-obvious nature should also be explained via comments if possible. Trivial code does not need to be commented. For example 

`x = 5 # this is a variable which we set to x` 

Is redundant and pointless. 

## Documentation
All project files should have a corresponding documentation file, explaining the purpose of the project file, as well as containing a reference on how to use it, a function reference, and a class reference. Proper style may be observed [here](libhsm.md).