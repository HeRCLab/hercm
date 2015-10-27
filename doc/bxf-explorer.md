# This page is under construction

This page is incomplete. In the future, more detailed explanations, and usages examples and tutorials will be included. 

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