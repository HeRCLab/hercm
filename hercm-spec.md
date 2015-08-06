# The HeRCM file format specification
## Introduction
The HeRCM (HeRC Matrix) file format was created to store compressed arrays, for later reading into other software. The format is specifically designed to be simple, fast to read, and easy to understand and parse. File size and initial conversion overhead were not major design concerns however. 

## Layout
A HeRCM file is laid out into various sections. Each section has one header, which contains no spaces and is terminated by a `\n` character. Each section contains one field, which contains one or more items, each separated by a space, and terminated with a `\n` character. The last line of a HeRCM file is always `END`. A HeRCM file is organized into the following sections. 

### Header
The first line of a HeRCM file is the header. A valid header contains the string "HERCM FILE", followed by the format as a three character string 
Currently, the following formats are valid: 

* `CSR` 

The header should also contain the width, height, and number of non zero entries, in that order, separated by whitespace. 

Finally, the header should contain an indicator for the symmetry of the matrix. Valid options are: 

* `SYM` - the matrix is symmetrical
* `ASYM` - the matrix is asymmetrical

An example of a valid header would look like this: 
```
HERCM FILE CSR 5 5 8 ASYM
```

This example would be valid for a 5 x 5 CSR matrix, with 8 non-zero entries, which is asymmetrical.  

### VAL
The val field should contain one or more integers, each being a non zero value in the matrix. NoteThe way in which CSR val fields wrap; as an example, for the matrix: 

```
1 2 3 
4 5 6
7 8 9
```
The VAL field would look like this:
```
VAL
1 2 3 4 5 6 7 8 9
```

### ROWPTR
The row_ptr field should contain one or more integers, indicating which indexes of the VAL field are the *first* nonzero value of a *new* row. Note that all HeRCM vectors are zero-indexed.  

### COLIND 
The column index filed should contain the same number of integers as the val field. Each integer should represent the column of it's corresponding value. For example: 
```
VAL
1 2 3 4
...
COLIND
1 2 1 2
```
Would indicate that the zeroth index of VAL goes in column 1, the first index of VAL goes in column two, the second index of VAL goes in column 1, and the third index of VAL goes in column 2. 

## Example 
```
1    0      0       6      0     
0   10.5    0       0      0     
0    0    .015      0      0     
0  250.5    0     -280    33.32  
0    0      0       0     12 
```

The above matrix may be reproduced by the valid HeRCM file below. 
```
HERCM FILE CSR 5 5 8 ASYM
VAL
1.0 6.0 10.5 0.015 250.5 -280.0 33.32 12.0 
ROWPTR
0 2 3 4 7 8
COLIND
0 3 1 2 1 3 4 4 
END


```