# HeRC Matrix Tools (HeRCM)

# Introduction
**ATTENTION**: This project is still under active development. While most of the code has been tested for basic functionality, performance and edge cases have not been evaluated yet. 

HeRC Matrix Tools is a collection of open source sparse and symmetric matrix tools, originally created for the University of South Carolina HeRC research group. 

# Tools
## Better Matrix Format (BXF)
Better Matrix Format (previously called "HeRCM format", with the `.hercm` file extension) is a simple matrix storage format, which stores COO-compressed sparse matrices in a human-readable and writable format. BXF tries to avoid unneeded complexity by utilizing a simple, rigid file format.

For more information, review the [bxf specification](doc/bxf-spec.md). 

## BXFExplorer
BXFExplorer (formerly "HeRCM Explorer") is a tool which can be used for interacting with sparse matrix files. It can read and write matrices in a variety of formats, including `.bxf`, `.mtx`, and `.mat` formats. 

For more information, review the [BXFExplorer documentation](doc/bxf-explorer.md)

## libHercMatrix 
libHercMatrix, (formerly "libhsm") provides the class object used by HeRCM Python code to store matrices. It also provides a variety of helper functions for manipulating said matrices, and providing interoperability with scipy/numpy. Note that libHercMatrix uses numpy internally via a custom dtype, and is fully inter-operable with scipy sparse-matrix data types. 

## libBXF
libBFX (formerly part of "libSparseConvert") provides Python functions for storing and loading BXF files. 

## libHercmIO 
libHercmIO (formerly part of "libSparseConvert") provides Python functions for storing and loading matrices in a variety of formats. It uses libBXF as a back-end for `.bxf` files, and various other tools and libraries for other matrix formats.

## bxfio
bxfio (formerly "hercmio") provides methods for storing and loading matrices in `.bxf` format via C++98. 

# Support status 

## File formats

| file format | status | provided by | maintainer | notes |
|-------------|--------|-------------|------------|-------|
| `.bxf` | fully supported | in-house | Charles Daniels | |
| `.hercm` | fully supported | in-house | Charles Daniels | `.hercm` was the original name for `.bxf`, so both formats can be read in exactly the same way | 
| `.mtx` | fully supported | [scipy.io](http://docs.scipy.org/doc/scipy/reference/io.html) | N/A | | 
| `.mat` | fully supported | [scipy.io](http://docs.scipy.org/doc/scipy/reference/io.html) | N/A | | 
| `.valcol` | support planned | in-house planned | N/A | | 
| Harwell-Boeing | support planned | in-house planned | N/A | | 

## Programming languages

| language | read bxf | write bxf | read other | write other | development status | maintainer | 
|----------|----------|-----------|------------|-------------|--------------------|--------------|
| Python 3.x | yes | yes | yes: mtx, mat | yes: mtx, mat | in progress | Charles Daniels |
| C++ 98 | yes | yes | no; valcol palnned | no | in progress | Charles Daniels 

Additionally, support is planned for C and Python 2.7.X in the future (pull requests welcome!) 

# New features in release 0.2 Alpha

## New matrix summery view 
Supports arbitrary number of elements to best fit any terminal (default is 10 elements by 10 elements) 

example:
```
> display 4 4
  3e+06       0  ...       0       0
      0   2e+06  ...       0       0

      0       0  ...   1e+09  -1e+08
      0       0  ...  -1e+08   5e+08
> display 12 12
  3e+06       0       0       0   1e+06   2e+06  ...       0       0       0       0       0       0
      0   2e+06       0  -2e+06       0   6e+06  ...       0       0       0       0       0       0
      0       0   2e+06  -2e+06  -3e+06       0  ...       0       0       0       0       0       0
      0  -2e+06  -2e+06   1e+09       0       0  ...       0       0       0       0       0       0
  1e+06       0  -3e+06       0   1e+09       0  ...       0       0       0       0       0       0
  2e+06   6e+06       0       0       0   2e+09  ...       0       0       0       0       0       0

      0       0       0       0       0       0  ...   6e+04       0       0       0   2e+06   1e+05
      0       0       0       0       0       0  ...       0   4e+06   5e+05  -5e+06       0       0
      0       0       0       0       0       0  ...       0   5e+05   5e+06   1e+05       0       0
      0       0       0       0       0       0  ...       0  -5e+06   1e+05   2e+09       0       0
      0       0       0       0       0       0  ...   2e+06       0       0       0   1e+09  -1e+08
      0       0       0       0       0       0  ...   1e+05       0       0       0  -1e+08   5e+08
```

## New `csrdisplay` output format
Automatically calculates the row of each index, while still displaying the contents of `row_ptr`. Allows viewing of a particular range of rows, or the whole matrix. 

example - viewing rows 4 through 6: 
```
> csrdisplay 4 6
WARNING: matrix contains more than 25 entries,
are you sure you wish to proceed?
(yes/no)> yes
index  value      column  row_ptr row
   30  1.1e+09       4      30       4
   31   -1e+06       6               4
   32    2e+08      10               4
   33  2.8e+06      20               4
   34  3.3e+08      22               4
   35 -8.3e+05      28               4
   36  1.5e+09       5      36       5
   37   -2e+06      11               5
   38 -5.6e+06      19               5
   39  6.7e+08      23               5
   40 -2.1e+06      24               5
   41    1e+08      29               5
   42  2.8e+06       6      42       6
   43   -1e+06      10               6
   44  2.1e+06      11               6
   45 -2.8e+06      12               6
   46 -2.9e+04      30               6
   47  2.1e+06      35               6
```
## New help system

Allows for per-command help. Running commands without required arguments, or with incorrect types will generate useful output. 

example
```
> help load
----------------------------------------
load [path]  [format]
-- arguments --
    [path] <class 'str'> -  The file to load
    [format] <class 'str'> -  The format of said file
-- use --
    Reads in the file for viewing and manipulation
> load example.txt
ERROR, incorrect number of arguments for load
Missing argument 'format' at position 1
> csrdisplay foo bar
ERROR: argument {0} was present, but of type {1}  not required type <class 'int'>
```

## Improved formatting for `col` and `row`

example

```
> col 0
col 0, row 0: 2832268.51852
col 0, row 4: 1000000.0
col 0, row 5: 2083333.33333
col 0, row 6: -3333.33333333
col 0, row 10: 1000000.0
col 0, row 18: -2800000.0
col 0, row 24: -28935.1851852
col 0, row 29: 2083333.33333
> row 0
col 0, row 0: 2832268.51852
col 4, row 0: 1000000.0
col 5, row 0: 2083333.33333
col 6, row 0: -3333.33333333
col 10, row 0: 1000000.0
col 18, row 0: -2800000.0
col 24, row 0: -28935.1851852
col 29, row 0: 2083333.33333
```

## Improved formatting for `range`

example
```
> range 2 2 5 5
 1.72e+06 -2.08e+06 -2.78e+06         0
-2.08e+06     1e+09         0         0
-2.78e+06         0  1.07e+09         0
        0         0         0  1.54e+09
```
