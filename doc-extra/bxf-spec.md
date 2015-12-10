# The BXF file format specification, revision 2.2
# Introduction
The BXF (Better Matrix Format, formerly named "HeRCM") file format was created to store compressed arrays, for later reading into other software. The format is specifically designed to be simple, fast to read, and easy to understand and parse. File size and initial conversion overhead were not major design concerns however. 

All BXF files should be stored in row-major format. If the matrix is symmetric, the upper triangle is always stored. 

# Layout
A BXF file has two sections. The first section contains one line, and is the header, containing key information about the matrix. 

The second sections contains several fields, enumerated below. 

##Fields 
A field contains a header, on it's own line, and is terminated by `ENDFIELD` on it's own line. A field may contain one or more entries, delineated by whitespaces. Newlines are ignored when parsing field contents. By convention, fields should contain at most ten entries per line. 

Field headers take the format `NAME VTYPE`, where `NAME` can be any string, and `VTYPE` indicates the variable type of the field, and can be either `FLOAT`, `INT`, or `STRING`. Unlike previous BXF versions, BXF 2.1 fields are *always* lists, even if they contain only one element. 

**NOTE**: BXF does not differentiate between float and double, and either may be written to a `FLOAT` field. It is up to the parser to determine how to read in `FLOAT` fields. 

All of the following are valid examples of fields. 
```
EXAMPLEFIELD STRING
foo bar baz
ENDFIELD
```
```
EXAMPLEFIELD STRING
foobar
ENDFIELD
```
```
EXAMPLEFIELD INT
5
ENDFIELD
```
```
EXAMPLEFIELDFLOAT 
7.5 3 9.0 3.56
ENDFIELD
```

## Header
The first line of a BXF file is the header. Header contents are enumerated below...

| position | purpose | valid values |
|----------|---------|--------------|
| 0        | version specifier | a BXF version identifier string |
| 1        | width of matrix | any nonnegative integer |
| 2        | height of the matrix | any nonnegative integer | 
| 3        | number of nonzero elements | any nonnegative integer |
| 4        | matrix symmetry | `SYM` or `ASYM` | 

**NOTE**: positions are whitespace delineated 

**TODO**: add an example

## BXF versions & identifier strings

| version name | identifier | status |
|--------------|------------|--------|
| BXF 1.0      | `HERCM`    | merged with BXF 2.0 |
| BXF 2.0      | `BXF  `    | deprecated          |
| BXF 2.1      | `BXF21`    | depreciated *       |
| BXF 2.2      | `BXF22`    | in development      |

`*` - indicates a format which has never appeared in any stable release of 
of HeRCM (usually indicated a format which was discarded before development
was completed)

**NOTE**: until BXF 2.2 symmetric matrices were stored in the upper triangle, 
rather than the lower triangle. 


## Required Fields 
A valid BXF file used for storing sparse matrices must have several specific fields, which follow. Note that BXF always stores matrices in COO format for easy conversion to CSR, CSC, and for easy per-index access. 

### `REMARKS LIST STRING` 
Effectively a comments field. This field is ignored by any compliant parser, and may contain any content the creator of the file desires. 

### `VAL LIST FLOAT`
The `val` vector for a COO matrix. 

### `ROW LIST INT`
The `row` vector for a COO matrix, sometimes referred to as `row_ind`, or `row_ptr`. 

### `COL LIST INT`
The `col` vector for a COO matrix, sometimes referred to as `col_ind`, or `col_ptr`. 

## Verification sum
**TODO**

# Symmetric matrices 
By convention, a symmetric BXF formatted matrix file must store **only** the **lower** triangle. In previous versions, the upper triangle was stored, however the lower triangle has superior characteristics for certain types of sparse matrix operations. Additionally, compliant io implementation are encouraged, but not required to provide methods to read the upper triangle. 

**NOTE**: If an io implementation provides methods for reading the upper triangle, it should also provide a method for sorting the matrix to row-major, as many third party libraries assume sparse matrices are stored in row major format - simply performing a transpose operation by switching row and col is not enough. 

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
VAL FLOAT
4.0 2.0 1.0 5.0 7.0 6.0 3.0 8.0
ENDFIELD
ROW INT
0 0 1 2 2 3 3 3
ENDFIELD
COL INT
0 3 1 2 3 0 1 3
ENDFIELD
```

The full BXF file for this matrix follows. 

```
BXF22 4 4 8 ASYM
REMARKS STRING
ENDFIELD
VAL FLOAT
4.0 2.0 1.0 5.0 7.0 6.0 3.0 8.0
ENDFIELD
ROW INT
0 0 1 2 2 3 3 3
ENDFIELD
COL INT
0 3 1 2 3 0 1 3
ENDFIELD
```

# References 
* [Sparse Data Structures](http://amath.colorado.edu/sites/default/files/2015/01/195762631/SparseDataStructs.pdf)