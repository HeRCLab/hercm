# Introduction
libhsm, (HSM is an abbreviation for HeRC Sparse Matrix), is a python library containing a class which may be used to contain HeRCM formatted matrices. libhsm stores said matrices internally in the dict variable `contents`, and also permits access in any format supported by `scipy.sparse.coo_matrix.asformat()`. An example of the `contents` variable when populated follows. 

```
{'col': [4, 4, 3, 2, 1, 4, 2, 1],
'height': 5,
'nzentries': 8,
'remarks': [],
'row': [4, 3, 3, 4, 1, 1, 2, 4],
'symmetry': 'ASYM',
'val': [8.0, 7.0, 5.0, 3.0, 4.0, 2.0, 1.0, 6.0],
'verification': 7.0,
'width': 5}
```

# Function Reference
## `hsm` 
`hsm` takes no arguments to `__init__()`. 

### def getInFormat(this, format):
* `format` - a string containing any valid arguments for `scipy.sparse.coo_matrix.asformat()`. Some examples include `coo`, `csr`, and `csc`. 

Returns contents as a `scipy.sparse` matrix of the desired type. 

### def getValue(this, row, col, assumeRowMajor=False):
* `row` - int row of desired value
* `col` - int column  of desired value
* `assumeRowMajor` - bool indicating whether or not to assume the matrix is already in row major form

Returns the value at `row`,`col` in the matrix (zero indexed), or None if the value cannot be found. If `assumeRowMajor` is True, a somewhat optimized version of the algorithm will be used. However, if `assumeRowMajor` is True and the matrix is not row major, results will most likely be incorrect (possibly in non-obvious ways). 

def setValue(this, newRow, newCol, newVal, assumeRowMajor=False):
* `newRow` - int row of value to set
* `newCol` - int col of value to set
* `newVal` - float value of element to set 
* `assumeRowMajor` - bool indicating whether or not to assume the matrix is already in row major form

Sets the value at row `newRow` and column `newCol` equal to `newVal`. If `newVal` is zero, it will be removed from the matrix. If the previous value of the element was zero, a new element will be appended to the matrix. Note that `setValue()` may modify the matrix in such a way that the matrix is no longer row major. 

### def removeZeros(this):
Removes any zero elements of the matrix (missing elements in COO are assumed to be zero). 


### def makeRowMajor(this): 
Converts the matrix stored in the HSM instance to row major form. 