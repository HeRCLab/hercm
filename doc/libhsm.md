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

### def getValue(this, row, col):
* `row` - int row of desired value
* `col` - int column  of desired value

Returns the value at `row`,`col` in the matrix (zero indexed), or None if the value cannot be found. 