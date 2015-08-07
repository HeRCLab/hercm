# Introduction
The HeRCMio c++ reference implementation is written in c++98, and has no dependencies. 

# Compiling 
The library comes with a make file. To compile the example, use `make hercmio-example`. HeRCMio can also be compiled to a .o or .so file directly with `make hercmio.o` or `make hercmio.so`, respectively. 

# Caveats and known issues 
* `REMARKS` field is ignored entirely, meaning any comments will be lost if a matrix is read then written . 
* field's c and v type are not checked. For example, HeRCMio will always read VAL as floating point, even if it is populated with ints, and it's header adjusted accordingly. 
* `makeRowMajor()` uses a type of bubble sort, and will probably be slow on large matrices

# hercmio-example
hercmio-example is a small c++98 program included with HeRCMio for the purpose of testing, and to demonstrate proper calling conventions. Instructions for compiling hercmio-example are above. Usage is as follows. 

```
hercmio-example usage:
help   - - - - display this message
read [file]  - reads hercm file [file], prints as csr
write [file] - writes the following matrix to [file]
 0 5 3
 2 9 4
 0 0 1
```

# Error checking
Most functions in HeRCMio that do not otherwise have useful return values will return `HERCMIO_STATUS_SUCCESS` on successful execution, and will return `HERCMIO_STATUS_FAILURE` on any error. Both are preprocessor definitions, which can be found in `hercmio.hpp`

# Function reference 
## bool checkVectorForString(vector<string> vectorToCheck, string stringToSearchFor)
* `vectorToCheck` - vector of strings to check 
* `stringToSearchFor` - a string to search `vectorToCheck` for 

Utility function, checks if any element of `vectorToCheck` exactly matches `stringToSearchFor`. Returns true if so, false otherwise. 

## int stringToInt(string sourceString)
* `sourceString` - a string to be cast to int 

Utility function, returns the string as an integer. On error, returns the int `-999999`. 

## float stringToFloat(string sourceString)
* `sourceString` - a string to be cast to float 

Utility function, returns the string as an float. On error, returns the float `-999999.0`. 

## vector<string> split(string str, char delimiter)
* `str` - the string to be split
* `delimiter` - the delimiter on which to split the string

Utility function. Similar to Python's `string.split()` method. Generates a vector of strings such that each element of the vector is a non-overlapping string, spanning the beginning of `str` to an instance of `delimiter`, two instance of `delimiter`, or an instance of `delimiter` and the end of `str`. Removes all instance of `delimiter`. No element of the return value will be an empty string (`""`). 

## int readHercmHeader(string fileName, int &width, int &height, int &nzentries, string &symmetry,float &verification)
* `fileName` - the name of the file from which to read the header
* `width` - an integer into which the width of the matrix will be read
* `height` - an integer into which the height of the matrix will be read 
* `nzentries` - an integer into which the number of non zero elements will be read 
* `symmetry` - a string, either `SYM` or `ASYM` indicating the matrix's symmetry
* `verification` - a float into which the verification sum will be read 

Reads the header of a HeRCM file and stores resulting data in the above variables, hence why they are passed by reference. Returns `HERCMIO_STATUS_SUCCESS` on successful read, and `HERCMIO_STATUS_FAILURE` on any failure. 

## int readHercm(string fileName, float * val, int * row, int * col)
* `fileName` - the name of the HeRCM file to read
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val` 

Reads the contents of the HeRCM file into `val`, `row`, and `col`, which correspond to the similarly-named fields outlined in the HeRCM spec. Returns `HERCMIO_STATUS_SUCCESS` on successful read, and `HERCMIO_STATUS_FAILURE` on any failure. 

## int readHercm(string fileName, double * val, int * row, int * col)
Overloaded version of `readHercm()`, which accepts `val` as a double instead. Otherwise identical. 

## bool checkIfSorted(int * vector, int size)
* `vector` - a 1 dimensional integer matrix 
* `size` - the number of elements in `vector`

Utility function. Returns true if `vector` is sorted from least to greatest, returns false otherwise. 

## bool checkIfRowMajor(int * row, int * col, int nzentries)
* `row` - a 1 dimensional int matrix, to be allocated with a number of elements equal to the number of nonzero elements in the matrix. 
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `row` 
* `nzentries` - the number of non zero elements in the matrix

Utility function. Checks if the COO matrix is in row major form. If so, returns true, otherwise returns false. Note that `val` is not required for this check at all. 

## int makeRowMajor(int * row, int * col, float * val, int nzentries)
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val` 
* `nzentries` - the number of non zero elements in the matrix

Utility function. Modifies the COO matrix stored in `val`, `row`, and `col` such that it is in row major form. Always returns `HERCMIO_STATUS_SUCCESS` 

## int makeRowMajor(int * row, int * col, double * val, int nzentries)
Overloaded version of `makeRowMajor()`, which accepts `val` as a double instead. Otherwise identical.

## int cooToCsr(int * row, int * col, float * val, int * ptr, int nzentries, int height)
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `ptr` - a 1 dimensional int matrix, to be allocated with a number of elements equal to the number of rows in the matrix 
* `nzentries` - the number of non zero elements in the matrix
* `height` - the number of row in the matrix as an int 

Generates the CSR `ptr` (sometimes `row_ptr`, `rowptr`, or `indptr`) array and stores it in `ptr` based on the contents of the COO matrix stored in `row`, `col`, and `val`. Always returns `HERCMIO_STATUS_SUCCESS`. 

## int cooToCsr(int * row, int * col, double * val, int * ptr, int nzentries, int height)
Overloaded version of `cooToCsr()`, which accepts `val` as a double instead. Otherwise identical.

## float generateVerificationSum(int * row, int * col, float * val, int nzentries)
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val` 
* `nzentries` - the number of non zero elements in the matrix

Calculates the verification sum of the matrix, as described in the HeRCM spec. Returns said value as a float. 

## float generateVerificationSum(int * row, int * col, double * val, int nzentries)
Overloaded version of `generateVerificationSum()`, which accepts `val` as a double instead. Otherwise identical.

## bool verifyMatrix(string inputFile, float * val, int * row, int * col)
* `fileName` - the name of the HeRCM file to read
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val` 

Calculates the verification sum of the COO matrix stored in `val`, `row`, and `col`. Reads the matrix's header and compares it with the calculated value. If the values match, returns true, otherwise returns false. Also returns false if the header cannot be read. 

## bool verifyMatrix(string inputFile, double * val, int * row, int * col)
Overloaded version of `verifyMatrix()`, which accepts `val` as a double instead. Otherwise identical.

## int writeHercm(string fileName, int height, int width, int nzentries, float * val, int * row, int * col, string symmetry, float verification)
* `fileName` - the string name of the file to be read 
* `height` - the number of rows in the matrix
* `width` - the number of columns in the matrix
* `nzentreis` - the number of non zero elements in the matrix 
* `val` - a 1 dimensional float matrix, to be allocated for a number of elements equal to the number of non zero entries in the matrix 
* `row` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `col` - a 1 dimensional int matrix, to be allocated with the same number of elements as `val`
* `symmetry` - a string `SYM` or `ASYM` indicating the symmetry of the matrix 
* `verification` - the verification sum of the matrix

Writes the COO matrix stored in `val`, `col`, and `row`, whose verification sum is `verification`, and whose dimensions are `width` x `height` to the file `fileName`. Returns `HERCMIO_STATUS_SUCCESS` on successful write, and `HERCMIO_STATUS_FAILURE` on any error. Always converts the matrix to row major form before writing. 


## int writeHercm(string fileName, int height, int width, int nzentries, double * val, int * row, int * col, string symmetry, float verification)

Overloaded version of `writeHercm()`, which accepts `val` as a double instead. Otherwise identical.
