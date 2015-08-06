# hercmio 

## Introduction
The hercmio library is a simple tool used to read and write data to HeRCM files. For more information on HeRCM files, please review the attached file `hercm-spec.md`. 
If you are not familiar with compressed matrix formats such as CSR, check out [this document](http://amath.colorado.edu/sites/default/files/2015/01/195762631/SparseDataStructs.pdf) 
to learn more. 
## Objectives 
The hercmio library was created with several key objectives in mind. Namely: 

* The library should be available to the widest possible array of systems and compilers. Therefore, it is entirely C++98 compliant, although it may throw warnings depending on which compiler is used.

* The library should handle as much overhead as possible for the application. For reads, all the caller needs to do is supply the filename and pointers to the val, row_ptr, and colind arrays.  

## Included Files 
### hercmio.cpp and hercmio.hpp
The library itself and the header file required to use it from other projects

### hercmio-example.cpp
A simple example of how hercmio may be used in a real world application. When compiled, hercmio-example can read hercm file and convert them to dense matrices, which it will then print to stdout. hercmio-example can also write hercm file, given a file containing a dense matrix. An example input file is included below.

```
1 2 3
4 5 6
7 8 9
```
Given this file, hercmio-example would write a separate file containing the same matrix in HeRCM format. 

### example_matrix 
An example dense marix for use with `hercmio-example`.

### example.mtx
An mtx formatted matrix, for use with `mtxparse.py`. 

### example_output.hercm 
An example hercm file, produced from example_matrix with `hercmio-example`. 

### hercm-spec.md 
A file detailing the HeRCM file format. 

### makefile 
A simple makefile, which will build `hercmio-example`. It should be simple enough that even users unfamiliar with GNU make should be able to understand how `hercmio-example` should be compiled. 

## Using hercmio
To include hercmio in your project, simply `#include "hercmio.hpp"`. 

### Read a HeRCM file
If you wish to read in a HeRCM file, you may do as follows. 

```cpp
#include "hercmio.hpp"

string fileName = "example_output.hercm" // you will probably want to get this from argv, but we will hardcode it for readability 
string format,symmetry; // needed by readHercmHeader()
int width, height, nzentries; // also needed by readHercmHeader()

readHercmHeader(fileName, format, width, height, nzentries, symmetry); // read the header to get info we will to initialize our arrays
// note that readHercmHeader accepts arguments passed by reference, hence the variables will already contain the data we need
// format contains the format of the matrix. At time of writing, only CSR is supported, but that may change. 
// width and height are the number of columns and number of rows in the matrix respectively 
// nzentries is the number of non zero entries in the matrix 

// create the arrays in which we will store the matrix
float val[nzentries];
int row_ptr[width+1];
int colind[nzentries]; 

readHercm(fileName, val, row_ptr, colind); 
// readHercm also accepts arguments by reference

```

That is all that is required to read a HeRCM file. The matrices and variables declared and set will include all the data you will need. 

### Write a HeRCM file
The `writeHercm()` function expects the matrix to already be CSR formatted, if not, review the section `Converting a dense matrix to CSR` below. Therefore, I will assume for this example you have already declared the variables 

* `val` 
* `row_ptr`
* `rowptr` 
* `height` (number of rows in matrix)
* `width` (number of columns in matrix)
* `nzentries` (number of non zero entries in matrix)
* `filename` (string name of the file you want to write to)
* `symmetry` (string indicating symmetry or asymmetry, one of `SYM` or `ASYM`)

Given that the above have been declared, and already contain the desired values for writing, you may write them to the file with the following. 

```cpp
writeHercm(filename, height, width, nzentries, val, row_ptr, colind, symmetry);
```
Your data should now be stored in the specified file, in HeRCM format. 

### Converting a dense matrix to CSR
If you are attempting to convert an mtx (matrix market) file to HeRCM, please check out the `mtxparse.py` utility. This section includes a simple algorithm to convert a dense matrix (example below) to CSR format. This example assume you have already stored the matrix in the variable `matrix`, which is a two dimensional array of floats, and that you have the matrix's width and height stored in variables of the same name. 

```
1    0      0       6      0     
0   10.5    0       0      0     
0    0    .015      0      0     
0  250.5    0     -280    33.32  
0    0      0       0     12 
```

The algorithm itself can be implemented as follows. 

```cpp
// first we need to count the number of nonzero entries, so we can declare our val and colind matrices later
int nzentries=0; 
for(int row=0; row < height; row++)
{
	for (int col=0; col < width; col++)
	{
		if (matrix[col][row] != 0)
		{
			nzentries++;
		}
	}
}

//here we declare our matrices for CSR
float val[nzentries];
int row_ptr[height+1];
int colind[nzentries];
int valCounter = 0; // keep track of what index of val we are writing to
int row_ptrCounter = 1;
row_ptr[0] = 0; // the below does not account for the first index of row_ptr
int tmp_ptr = 0; // this will be used to accumulate row_ptr values


for (int row=0; row < inputMatrixHeight; row++) // for each row
{
	for (int col=0; col < inputMatrixWidth; col++) // for each column 
	{
		float currentValue = inputMatrix[col][row]; // get the value at the current index 
		if (currentValue != 0.0) // if it is a non zero value
		{
			val[valCounter] = currentValue; // set the next index of value
			colind[valCounter] = col; // set colind 
			tmp_ptr++; 
			valCounter++; 
		}
	}
	row_ptr[row_ptrCounter] = tmp_ptr; // we are starting a new row, save our index
	row_ptrCounter++;
}

```

## Functions included in hercmio
This section details the usage and calling of each function in hercmio

### bool checkVectorForString(vector<string> vectorToCheck, string stringToSearchFor)

* `vectorToCheck` should be a vector of strings, which will be searched for instances of `stringToSearchFor`
* `stringToSearchFor` should be a string, for which `vectorToCheck` will be searched

Returns true if stringToSearchFor is an exact match for at least one entry in vectorToCheck, otherwise returns false. 

### int stringToInt(string sourceString)

* `sourceString` should be a string containing an integer only. Including non numeric characters may cause the program to terminate. 

Converts sourceString to an integer and returns it. Terminates program execution if conversion fails. 

### float stringToFloat(string sourceString)

* `sourceString` should be a string containing a float only. Including non numeric characters may cause the program to terminate. 

Converts sourceString to a float and returns it. Terminates program execution if the conversion fails. 

### vector<string> split(string str, char delimiter) 

* str should be a string, which will be split 
* delimiter should be a char, at each instance of which str will be split

Splits str at each instance of delimiter, then returns the result as a vector of strings. Even if there are multiple consecutive instances of delimiter, it will never create any entry which is empty. 

### void readHercmHeader(string fileName, string &format, int &width, int &height, int &nzentries, string &symmetry)

* `fileName` should be a string specifying the file name of the HeRCM file to be read
* `format` should be an empty string (it will be overwritten with the format of the matrix that is read)
* `width` should be an empty int, into which the number of columns in the matrix will be read
* `height` should be an empty int, into which the number of rows in the matrix will be read
* `nzentries` should be an empty int, into which the number of non-zero entries in the matrix will be read
* `symmetry` should be an empty string, into which the symmetry of the matrix will be read

Reads the header from the file specified in fileName. Extracts the format, width, height, and number of non zero entries and stores them in the appropriate variables. As they are passed by reference, no return value is needed. If the file has in incorrect or malformed header, or the file cannot be opened, program execution will terminate. 

### void readHercm(string fileName, float * val, int * row_ptr, int * colind)
* `fileName` should be a string specifying the file name of the HeRCM file to be read
* `val` should be an array of floats, which will be used to store the matrix in CSR format. `val` should be initialized with a number of fields equal to the number of non-zero entries in the matrix. 
* `row_ptr` should be an array of ints, which will be used to store the matrix in CSR format. `row_ptr` should be initialized with a number of fields equal to the number of rows in the matrix plus one. 
* `colind` should be an array of ints, which will be used to store the matrix in CSR format. `colind` should be initialized with a number of fields equal to the number of non-zero entries in the matrix. 

Reads the data from the file specified in fileName. Populates val, row_ptr, and colind appropriately for use as a CSR formatted matrix. `readHercm()` will gather the width, height, and nzentries on it's own. Note that val, row_ptr, and colind are passed by reference, and must already be instantiated with appropriate capacities. `readHercm()` will terminate program executions under the same conditions as `readHercmHeader()`. 

### void writeHercm(string fileName, int height, int width, int nzentries, float * val, int * row_ptr, int * colind, string symmetry)

* `fileName` should be a stirng specifying the file name to be written. Note that `writeHercm()` will not append the `.hercm` file extension automatically, so you should specify it manually in the file name if you so desire. 
* `height` should be an int containing the number of rows in the matrix
* `width` should be an int containing the number of columns in the matrix
* `nzentries` should be an int containing the number of non-zero entries in the matrix
* `val` should be a CSR val matrix. `val` should be a matrix of floats. 
* `row_ptr` should be a CSR row_ptr matrix (sometimes referred to as ptr). `row_ptr` should be a matrix of ints.
* `colind` should be a CSR colind matrix. `colind` should be a matrix of ints. 
* `symmetry` should be a string containing either `SYM` or `ASYM` indicating the matrix's symmetry

Writes the data suppliedi n val, row_ptr, and colind to the file specified in fileName. height, width, and nzentries are also required in order to construct the header. While val, row_ptr, and colind are passed by reference, they are not modified. If `writeHercm()` fails to open the target file for writing, program execution will terminate. 

## License
mtxparse is liscensed under the BSD 3-clause license. The copyright holder is Charles Daniels, who may be reached at `cdaniels[at]fastmail[dot].com`. 

### mtxparse contributors
mtxparse was created by Charles Daniels in 2015. Additional contributors should be noted here as needed.