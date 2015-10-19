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

