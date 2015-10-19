# This page is under construction

This page is incomplete. In the future, more detailed explanations, and usages examples and tutorials will be included. 

# Help Message

help - display this message

log / log [N] - prints the libSparseConvert log. If [N] is specified, print only
 the most recent [N] lines. 

load [path] [format] - loads the file at [path] with the format [format]. 
[format] should be mtx or hercm.

write [path] [format] - writes the matrix to the file at [path] using the format
[format], which is mtx or hercm. Will silently overwrite any existing file at
[path]. 

info - prints information on the matrix 

display - prints the entire matrix to the console in dense form

csrdisplay - prints the matrix in csr format to the console 

raw - prints the raw hercm matrix to the console 

value [row] [col] - prints the value at [row],[col]

row [row] - prints all non-zero values in the given row

col [col] - prints all non-zero values in the given col

range [r1] [c1] [r2] [c2] - prints all elements, zero or nonzero, which lie 
between the upper left bound [r1],[c1], and the lower right bound [r2],[c2]

touch [row] [col] [val] - changes the value at [row] [col] to [val] 

paint [x1] [y1] [x2] [y2] [val] - works the same way as range, but changes
all values encountered to [val]

paint-diag [begin] [end] [spread] [value] / 
paint-diag [begin] [end] [spread] [value] [offset] - paints the value [value]
at all indices along the diagonal, from the [begin]th to the [end]th. Paints 
[spread] values to either side of said diagonal. Offsets the diagonal by 
[offset] columns, if [offset] is given. 

row-major - makes the matrix row major 

rmzeros - remove zeros from matrix

setdims [height] [width] - sets the dimensions of the matrix to height by width

setsym [symmetry] - sets symmetry. Will not change array elements, only modifies 
symmetry attribute. 

init / init [height] [width] / init [height] [width] [val] - sets matrix to
a blank 5x5 matrix of zeros. If height and width are supplied, matrix is set to
those dimensions. If val is supplied, initialize matrix elements to val.
Overwrites any already loaded matrix. 

gen-verification - updates verification sum to permit writing out matrix after 
modification. 

check-symmetry - check the symmetry attribute, and searches for any non zero
elements in the bottom triangle, printing the first five if they exist. 

plot - plots the matrix graphically using matplotlib 

head [file path] - prints the first 10 lines of file at [file path]

cat [file path] - prints all lines from [file path] 

ls - get directory listing

pwd - print current working directory 

exit - exits the program