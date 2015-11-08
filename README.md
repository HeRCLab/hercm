# HeRC Matrix Tools (HeRCM)

# Introduction
**ATTENTION**: This project is still under active development. While most of the code has been tested for basic functionality, performance and edge cases have not been evaluated yet. 

HeRC Matrix Tools is a collection of open source sparse and symmetric matrix tools, originally created for the University of South Carolina HeRC research group. 

HeRC Matrix Tools encompasses a number of tools and libraries to make working with symmetric matrices easier, enumerated below. 

## Matrix Explorer
Wraps most libraries and functionalities provided by the hercm project within a command line interface. Includes the ability to read and write matrices in a variety of formats, preview or plot matrices, and perform a variety of operations on them. 

## libHercmIO (python)
Aggregate IO library for hercm python code, wraps code to read and write matrices in all formats support by hercm python code. 

## libHercmIO (C++98)
Provides BXF IO for C++, with read-only valcol support planned. 

## libBXF 
Provides read/write access to bxf format files. 

## libValcol
Provides read/writ access to valcol format files. 

## libHercMatrix
Provides a feature rich class type for sparse matrices, and includes scipy/numpy interoperability. 

## matrixUtils
Provides user-interface centric utilities pertaining to sparse matrices, generally used almost exclusively by MatrixExplorer, but is provided as a separate library to facilitate automation by other scripts and programs. 

