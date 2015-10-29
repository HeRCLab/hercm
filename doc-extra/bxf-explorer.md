# BXF Explorer
BXF Explorer is a tool for manipulating sparse matrices, and for converting them between different formats. It includes the a ability to perform complex operations, such as painting a range of elements along a diagonal to a particular value.

# Interface
BXF Explorer includes an simple, yet powerful command line interface. Whenever you see the prompt `> `, BXF Explorer is ready to accept your input. Input consists of three parts: the *command*, *required arguments*, and *optional arguments*. 

## Commands 
A command is the first space-delineated string from an input. For example:

**figure 1**
```
load myMatrix.bxf bxf
```

`load` is the command in the above example. 

## Required Arguments
Required arguments, as the name implies, are required in order to execute a command. All arguments are space-delineated, and are order-sensitive. In **figure 1** above, `myMatrix.bxf` and `bxf` are examples of arguments, and both happen to be required to run the `load` command. 

## Optional Arguments
Optional arguments provide access to extended functionality of various commands. Optional arguments are also order-sensitive, and begin after the required arguments of a command. For example: 

**figure 2**
```
paint 0 0 10 10 734
```

* `paint` is the command
* `0 0 10 10` are the required arguments
* `734` is an optional argument

If optional arguments are not given, a default value will be assumed, and the command will execute anyway. 

# Getting Help
BXF Explorer includes a robust help system. You can view help for all commands with `help`, and you can view help for a specific command with `help command`. The following conventions are used:

* all arguments are in order 
* all required arguments are surrounded by brackets `[]` 
* all optional arguments are surrounded by parens `()` 

For a convenience, the full output of `help` is provided below in the **Help Message** section. 

## Interpreting errors 
As you use BXFExplorer, you will probably make some errors, which are enumerated below.

### `ERROR, incorrect number of arguments for command` 
The command you are trying to run requires more arguments than you are giving it. Review the command's help page with `help command` 

### `Missing argument 'argumentname' at position X` 
You are missing the argument identified by it's name. Note that positions are zero-indexed. For example, the first argument after the command would be position 0. 

### `ERROR: argument X was present, but is not of required type <class 'someclass'>`
This argument must be typecast to a specific type, such as an integer or floating point number, and the argument you provided was not valid, or could not be typecast to that type. 

### `WARNING: command is not in commandInfo, cannot check required arguments!` 
No help pages are available for this command, so BXFExplorer cannot check if you have provided correct argument. This message may be present on development versions of BXFExplorer where new commands have been implemented, but have not yet been documented. 

### `ERROR: Command not recognized` 
The command you are trying to run does not exist. Ensure you have spelled the command correctly. 

# Creating new commands - the commandInfo data format, and BXFUtils.py
If you are a developer, you may wish to implement a new command. If you decide to do so, you should consider the following conventions. 

* Add you command to BXFExplorer with an if statement, in the same style as the existing commands. 
* Command logic should go in a function in `BXFUtils.py`, which should then be called by said if statement. 
* The exception to the above is wrappers to existing functions (eg. `makeRowMajor()`)
* It is okay to do argument preparation/validation in `BXFExplorer`
* Functions in `BXFUtils.py` should not throw exceptions, and should do any needed exception handling themselves. 
* BXFEXplorer will do basic argument validation for you - it will ensure required arguments are present, and *it will automatically typecast argument to the desired type* - you *do not* need to typecast arguments yourself. 

## The commandInfo data structure 
commandInfo is a large data structure, which currently lives in `commandInfo.yaml`, which stores all information about all commands - including arguments, their required types, and help messages. commandInfo is a dict, each key is the name of a command,  and the data associated with the keys should look like this: 

```
{'argumentInfo': ['description of 1st required arg',
        'description of optional argument'],
 'help': 'This is the help message for the command',
 'optionalArguments': [[0, str, someArgument]],
 'requiredArguments': [[0, <class 'str'>, 'aRequiredArgument']]}
```

### `argumentInfo` 
A list contain strings, which are one-line descriptions of each argument in order. Both optional and required argument descriptions live here, with the required arguments first, and the optionals second. 

### `help` 
A string of any length containing the help text for the command. 

### `optionalArguments`
None, or a list of lists. Each sub-list contains it's position (position after the command for required arguments, or position after the required arguments for optional arguments), the python class to which the argument will be typecast, and a short (1 - 2 word) name for the argument. 

## `requiredArguments` 
Exactly the same format as optional arguments. 

# Help Message
```
----------------------------------------
paint [col1]  [row1]  [col2]  [row2]  (val)
-- arguments --
    [col1] <class 'int'> -  column of top-left corner
    [row1] <class 'int'> -  row of top-left corner
    [col2] <class 'int'> -  column of bottom-right corner
    [row2] <class 'int'> -  row of bottom-right corner
    (val) - <class 'float'> new value for elements
-- use --
    Modifies the values of the rectangular range of elements whose top-
    left corner is (col1, row1) and whose bottom right corner is (col2,
    row2). If val is given, elements are set equal val, otherwise they are
    set to zero
----------------------------------------
raw
-- arguments --
-- use --
    display the raw COO format data for the matrix
----------------------------------------
info
-- arguments --
-- use --
    Prints information about the loaded matrix
----------------------------------------
transpose
-- arguments --
-- use --
    Reflects the matrix about the diagonal
----------------------------------------
col [col]
-- arguments --
    [col] <class 'int'> -  the row to display
-- use --
    Displays all elements in the specified column
----------------------------------------
paint-diag [begin]  [end]  [spread]  [val]  (offset)
-- arguments --
    [begin] <class 'int'> -  the first column of the diagonal
    [end] <class 'int'> -  the last column of the diagonal
    [spread] <class 'int'> -  the number of indices on either side of the diagonal to paint
    [val] <class 'float'> -  the value to paint
    (offset) - <class 'int'> the number of indices to the left or right to offset the diagonal
-- use --
    sets all elements along the diagonal of the matrix to val, aswell as
    spread values to either side of the diagonal, starting column begin,
    and ending with column end. The diagonal can also be offset by offset
    elements to the left or right
----------------------------------------
row [row]
-- arguments --
    [row] <class 'int'> -  the row to display
-- use --
    Displays all elements in the specified row
----------------------------------------
check-tril
-- arguments --
-- use --
    Prints whether or not there are nonzero elements in the lower triangle
----------------------------------------
ls (path)
-- arguments --
    (path) - <class 'str'> the path to get a listing for - default is ./
-- use --
    Prints a directory listing for the specified path
----------------------------------------
load [path]  [format]
-- arguments --
    [path] <class 'str'> -  The file to load
    [format] <class 'str'> -  The format of said file
-- use --
    Reads in the file for viewing and manipulation
----------------------------------------
row-major
-- arguments --
-- use --
    Makes the matrix row-major (only affects COO data, not the contents of
    the matrix)
----------------------------------------
touch [col]  [row]  [val]
-- arguments --
    [col] <class 'int'> -  the column of the target element
    [row] <class 'int'> -  the row of the target element
    [val] <class 'float'> -  the new value for the element
-- use --
    Modifies the value of the matrix at the specified row and col
----------------------------------------
init [with]  [height]  (val)
-- arguments --
    [with] <class 'int'> -  the width for the new matrix
    [height] <class 'int'> -  the height for the new matrix
    (val) - <class 'float'> the value to initialize all elements in the new matrix to
-- use --
    Creates a new matrix with specified dimensions, with all elements
    initialized to zero, or to val if it is given
----------------------------------------
head [path]  (lines)
-- arguments --
    [path] <class 'str'> -  the path to the file to get the head of
    (lines) - <class 'int'> the number of lines to print from the file, default is 10
-- use --
    Prints the first lines lines of the file
----------------------------------------
pwd
-- arguments --
-- use --
    Prints the current working directory
----------------------------------------
plot
-- arguments --
-- use --
    Plots the matrix graphically with matplotlib
----------------------------------------
gen-verification
-- arguments --
-- use --
    Updates the verification sum of the loaded matrix
----------------------------------------
display (height)  (width)
-- arguments --
    (height) - <class 'int'> maximum number of elemets to display vertically
    (width) - <class 'int'> maximum number of elements to display horizontally
-- use --
    Displays a visualization of the matrix. If the matrix is very large,
    only the corners will be displayed
----------------------------------------
convert [source]  [source format]  [destination]  [destination format]
-- arguments --
    [source] <class 'str'> -  The path to the source file
    [source format] <class 'str'> -  the file format of the source file
    [destination] <class 'str'> -  the path to the destination file
    [destination format] <class 'str'> -  the format of the destination file
-- use --
    Reads the source file in the specified format, then writes itback out
    at the specified destination in the destination format
----------------------------------------
shell
-- arguments --
-- use --
    Drop to Python debugging shell. WARNING: INTENDED FOR DEBUGGING USE
    ONLY
----------------------------------------
check-symmetry
-- arguments --
-- use --
    Checks the symmetry attribute of the matrix, and whether or not the
    data in the matrix is actually symmetrical
----------------------------------------
cat [path]
-- arguments --
    [path] <class 'str'> -  The file to print all lines from
-- use --
    Prints all lines from the file
----------------------------------------
setdims [with]  [height]
-- arguments --
    [with] <class 'int'> -  the new width for the matrix
    [height] <class 'int'> -  the new height for the matrix
-- use --
    Changes the dimensions of the matrix, truncating elements which become
    out of bounds
----------------------------------------
cd [path]
-- arguments --
    [path] <class 'str'> -  new working directory
-- use --
    Changes the current working directory to path
----------------------------------------
range [col1]  [row1]  [col2]  [row2]
-- arguments --
    [col1] <class 'int'> -  column of top-left corner
    [row1] <class 'int'> -  row of top-left corner
    [col2] <class 'int'> -  column of bottom-right corner
    [row2] <class 'int'> -  row of bottom-right corner
-- use --
    Displays all elements in the rectangular region given by (row1, col1),
    (row2, col2)
----------------------------------------
write [path]  [format]
-- arguments --
    [path] <class 'str'> -  The file to write to
    [format] <class 'str'> -  The format of said file
-- use --
    Writes current matrix to specified file, in specified format note that
    the given path should include the desired file extension
----------------------------------------
exit
-- arguments --
-- use --
    exits the program
----------------------------------------
rmzeros
-- arguments --
-- use --
    Removes zero elements from the matrix (only affects COO data,  not the
    contents of the matrix)
----------------------------------------
csrdisplay (rowStart)  (rowEnd)
-- arguments --
    (rowStart) - <class 'int'> first row to display
    (rowEnd) - <class 'int'> last row to display
-- use --
    Displays the matrix as raw CSR data, prompts if nzentries > 25. if
    provided, will only display the CSR values between a particular range
    of rows in the matrix
----------------------------------------
setsym [symmetry]  (method)
-- arguments --
    [symmetry] <class 'str'> -  the new symmetry for the matrix
    (method) - <class 'str'> the algorithm to use
-- use --
    Makes the matrix symmetric or asymmetric, modifying COO data
    appropriately. By default, uses the truncate method. Available methods
    are: truncate - fastest, all elements from the bottom  triangle are
    removed/overwritten as needed; add - all elements in in the lower
    triangle are added to corresponding elements in the upper triangle
    (asym->sym) OR all elements in the upper triangle are added to the
    corresponding elements in the lower (sym->asym; smart - only
    overwrites values with are zero, very slow
----------------------------------------
value [column]  [row]
-- arguments --
    [column] <class 'int'> -  column of desired element
    [row] <class 'int'> -  row of desired element
-- use --
    display the value at column, row
----------------------------------------
help (command)
-- arguments --
    (command) - <class 'str'> specific command to retrieve help for
-- use --
    Prints help for all commands, or prints the help for the command
    specified in the first argument
```