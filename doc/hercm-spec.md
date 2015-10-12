# The HeRCM file format specification, revision 2.0
# Introduction
The HeRCM (HeRC Matrix) file format was created to store compressed arrays, for later reading into other software. The format is specifically designed to be simple, fast to read, and easy to understand and parse. File size and initial conversion overhead were not major design concerns however. 

All HeRCM files should be stored in row-major format. 

# Layout
A HeRCM file has two sections. The first section contains one line, and is the header, containing key information about the matrix. 

The second sections contains one or more fields. 

##Fields 
A field contains a header, on it's own line, and is terminated by `ENDFIELD` on it's own line. A field may contain one or more entries, delineated by whitespaces. Newlines are ignored when parsing field contents. By convention, fields should contain no more than ten entries per line, however a compliant parser should be able to handle any number of entries per line. 

Field headers take the format `NAME CTYPE VTYPE`, where `NAME` can be any string, `CTYPE` can be either `SINGLE` or `LIST`, indicating whether the field contains a list or a single value, and `VTYPE` indicates the variable type of the field, and can be either `FLOAT`, `INT`, or `STRING`. 

**NOTE**: HeRCM does not differentiate between float and double, and either may be written to a `FLOAT` field. It is up to the parser to determine how to read in `FLOAT` fields. 

All of the following are valid examples of fields. 
```
EXAMPLEFIELD LIST STRING
foo bar baz
ENDFIELD
```
```
EXAMPLEFIELD SINGLE STRING
foobar
ENDFIELD
```
```
EXAMPLEFIELD SINGLE INT
5
ENDFIELD
```
```
EXAMPLEFIELD LIST FLOAT 
7.5 3 9.0 3.56
ENDFIELD
```

## Header
The first line of a HeRCM file is the header. A valid header contains the string "HERCM" as it's first five characters. 

The header should also contain the width, height, and number of non zero entries, in that order, separated by whitespace. 

The header should contain an indicator for the symmetry of the matrix. Valid options are: 

* `SYM` - the matrix is symmetrical
* `ASYM` - the matrix is asymmetrical

Last, the header should contain the HeRCM verification sum, which is discussed in the later section

An example of a valid header would look like this: 
```
HERCM 5 5 8 ASYM 7
```

This example would be valid for a 5 x 5 CSR matrix, with 8 non-zero entries, which is asymmetrical.  

## Required Fields 
A valid HeRCM file used for storing sparse matrices must have several specific fields, which follow. Note that HeRCM always stores matrices in COO format for easy conversion to CSR, CSC, and for easy per-index access. 

### `REMARKS LIST STRING` 
Effectively a comments field. This field is ignored by any compliant parser, and may contain any content the creator of the file desires. 

### `VAL LIST FLOAT`
The `val` vector for a COO matrix. 

### `ROW LIST INT`
The `row` vector for a COO matrix, sometimes referred to as `row_ind`, or `row_ptr`. 

### `COL LIST INT`
The `col` vector for a COO matrix, sometimes referred to as `col_ind`, or `col_ptr`. 

## Verification sum
Every valid HeRCM 2.0 file must contain a verification sum, used to verify the validity of the file. The verification sum is generated as such: 

1. Sum the contents of `VAL`, call this A
2. Sum the contents of `ROW`, call this B
3. Sum the contents of `COL`, call this C 
4. Sum A, B, and C, call this D 
4. Modulo D by the number of non zero entries (indicated by the header), this the the verification sum. 

# Symmetric matrices 
By convention, a symmetric HeRCM formatted matrix file must store **only** the **upper** triangle. However, any fully compliant io implementation **must** provide methods for reading the upper triangle, lower triangle (extrapolated from the contents of the upper), and the entire matrix in asymmetrical format. This is because some 3rd party libraries expect asymmetric matrices, or matrices where the lower triangle is stored, rather than the upper. 

**NOTE**: it is also acceptable for io implementations to simple provide methods for getting the lower triangle or the asymmetric matrix after reading, if this is more convenient. 

# Example 
Consider the following matrix: 


```
4	0	0	2
0	1	0	0
0	0	5	7
6	3	0	8
```

The number of non zero entries in this matrix is 8, and the matrix is 4x4. The COO vectors for the matrix are as such:

```
VAL LIST FLOAT
8 7 5 3 4 2 1 6
ENDFIELD
ROW LIST INT
3 2 2 3 0 0 1 3
ENDFIELD
COL LIST INT
3 3 2 1 0 3 1 0 
ENDFIELD
```

The verification sum could be calculated as such: 
```
A = 36 (sum of val)
B = 22 (sum of row)
C = 21 (sum of col)
D = 79 (sum of A, B, and C)
result = 7 (nnz modulo D; 79 % 8)
```

We already know that this matrix is asymmetrical. 

Thus, the header would be: 

`HERCM 4 4 8 ASYM 7`

Thus, the full matrix could be reproduced as such: 
```
HERCM 4 4 8 ASYM 7 
REMARKS LIST STRING
This is an example matrix created for the HeRCM documentation. This field is ignored because it's title is REMARKS. 
ENDFIELD
VAL LIST FLOAT
8 7 5 3 4 2 1 6
ENDFIELD
ROW LIST INT
3 2 2 3 0 0 1 3
ENDFIELD
COL LIST INT
3 3 2 1 0 3 1 0 
ENDFIELD

```

# References 
* [Sparse Data Structures](http://amath.colorado.edu/sites/default/files/2015/01/195762631/SparseDataStructs.pdf)