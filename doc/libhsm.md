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
# Class reference 
## `libhsm.hsm`
|member functions |
|-----------------|
|`getInFormat()`  |
|`addElement()`   |
|`getElement()`   |
|`castElement()`  |
|`searchElement()`|
|`removeElement()`|
|`getValue()`     |
|`setValue()`     |
|`removeZeros()`  |
|`makeRowMajor()` | 

|constructor arguments|
|---------------------|
|					  |



## Function Reference
### def getInFormat(this, form):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`form`|string       |any format valid for scipy.sparse.coo_matrix.asformat() | N/A|

|return type|description|condition|
|-----------|-----------|---------|
|scipy.sparse|a scipy sparse matrix of the requested type|always|

|exceptions|cause| 
|----------|-----|
| | |

Gets the contents of the hsm instance in a given scipy.sparse format. 

### def addElement(this, element):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`element` |any supported by `castElement()`|the element to add to the matrix| N/A| 

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|Always|

|exceptions|cause| 
|----------|-----|
|ValueError|`castElement()` fails to cast one or more elements of `element`

### def getElement(this, n ,form=list):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`n`|int|index of element to retrieve|N/A| 
|`form`|list, numpy.void, or numpy.ndarray|format in which to return element|list|

|return type|description|condition|
|-----------|-----------|---------|
|list|list containing the `n`th element of the array in [row, col, val] format|`form` = list|
|numpy.void|numpy.void containing the `n`th element of the array in [row, col, val] format with the dtype `this.dtype`|`form` = numpy.void|
|numpy.ndarray|numpy array containing the `n`th element of the array in [row, col, val] format with a dtype `this.dtype`|`form` = numpy.ndarray|

|exceptions|cause| 
|----------|-----|
|IndexError|`n` is out of bounds for the array| 
|ValueError|`n` is not an int, or cannot be cast to an int|
|TypeError|form is not a valid type| 

Retrieves the `n`th element of the array in the desired format. Note that `form` should actually be `list` or another type. For example: 

```python
elem = HSM.getElement(index, list)
```

Values such as `"list"` will cause a TypeError. 


### def castElement(this, element):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`element`|list, numpy.void, or numpy.ndarray|element to be cast to numpy.ndarray|N/A|

|return type|description|condition|
|-----------|-----------|---------|
|numpy.ndarray|`element` cast to a numpy.ndarray|always|

|exceptions|cause| 
|----------|-----|
|ValueError|`castElement()` fails to cast any index of `element` to the needed type. May also be caused by passing a numpy.ndarray with a non-matching dtype and an invalid length|

Casts `element` to numpy.ndarray, mostly for use in other function that are part of libhsm.hsm. Note that if a numpy.ndarray is passed as `element`, and it's dtype matches `this.dtype`, it will be returned directly. If it's dtype does not match, it will be processed the same as a list. 


### def searchElement(this, element, rtol=1e-05, atol=1e-08):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`element`|any supported by `castElement()`|element to search for|N/A|
|`rtol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-05|
|`atol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-08|

|return type|description|condition|
|-----------|-----------|---------| 
|list|list containing all indices at which `element` occurs in the matrix|always|

|exceptions|cause| 
|----------|-----|
|ValueError|`castElement()` encountered a ValueError while casting `element`|

Search all elements in the COO matrix, and return all indices at which it occurs. Note the indices returned have no bearing on the element's physical location within the matrix. If no instances of the element are found, the return value is `[]`. 

Uses `numpy.isclose()` to compare `element` to matrix elements, to account for conversion between python and numpy floats, rounding errors, etc. Can search for exact matches by settings `rtol` and `atol` to zero. 

### def removeElement(this, n, rtol=0, atol=0):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`n`|int or any supported by `castElement()`|the index of the element to remove, or the element to remove|N/A|
|`rtol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-05|
|`atol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-08|

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
|ValueError|`castElement()` fails to cast the element|

Removes the desired element from the matrix, and updates `nzentries` accordingly. If `n` can be cast to int, or is an int, the `n`th element of the matrix will be removed. Otherwise, `n` is cast by `castElement`, then searched for by `searchElement` with `rtol` and `atol` set to 0. Each index at which `n` is thus found will be deleted. 



### def getValue(this, row, col, rtol=1e-05, atol=1e-08):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`row|`int|row of element|N/A|
|`col`|int|column of element|N/A|
|`rtol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-05|
|`atol`|float|passed through to [numpy.isclose](http://docs.scipy.org/doc/numpy-dev/reference/generated/numpy.isclose.html)|1e-08|


|return type|description|condition|
|-----------|-----------|---------|
|float|value stored at column `vol` and row `row`|always| 

|exceptions|cause| 
|----------|-----|
|IndexError|`col` or `row` is out of bounds for the matrix|


Returns the value stored at the given position in the matrix. Note that this means the actual coordinates within the dense matrix, **not** the value stored at the `n`th element of the matrix in COO format. 

### def setValue(this, newRow, newCol, newVal):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
|`newRow`|int|row of value to set|N/A|
|`newCol`|int|column of value to set |N/A|
|`newVal`|int|value to set|N/A|

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
|IndexError|`newRow` or `newCol` are out of bounds of the matrix|

Sets the value at row `newRow` and column `newCol` equal to `newVal`. If `newVal` is zero, it will be removed from the matrix. If the previous value of the element was zero, a new element will be appended to the matrix. Note that `setValue()` may modify the matrix in such a way that the matrix is no longer row major. 

### def removeZeros(this):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
| | | |

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
| | |


Removes any zero elements of the matrix (missing elements in COO are assumed to be zero). 


### def makeRowMajor(this): 
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
| | | |

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
| | |

Converts the matrix stored in the HSM instance to row major form. 

### def replaceContents(this, newContents):
|argument|expected type|description|default|
|--------|-------------|-----------|-------|
| newContents| any cast-able with `scipy.sparse.coo_matrix()` | new contents for instance | N/A

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
| | |

Replaces the instance's contents with any matrix which can be cast using `scipy.sparse.coo_matrix()`. Does not catch exceptions from `scipy.sparse.coo_matrix()`. 


### def makeSymmetrical(this, method='truncate'):

|argument|expected type|description|default|
|--------|-------------|-----------|-------|
| `method`| string | one of `truncate`, `add`, or `smart` describing method by which to make the matrix symmetrical | `truncate` |

|return type|description|condition|
|-----------|-----------|---------|
|None|N/A|always|

|exceptions|cause| 
|----------|-----|
| | |

Makes the HSM instance symmetrical. Does not change `this.verification` or `this.symmetry`, dealing only with the actual matrix as it is stored. Can change symmetry in one of three ways...

* `truncate` - all elements in the lower triangle of the matrix are discarded, only the upper triangle is stored 
* `add` - all elements in the lower triangle of the matrix are added to their corresponding elements in the upper. The diagonal is ignored. In other words the lower triangle is transposed and added to the upper.  
* `smart` - all elements in the lower triangle whose partner in the upper is not zero are deleted. Remaining elements are moved to the upper triangle with the `add` method. This method is very slow, taking `nzentries` * 2 iterations, plus the normal time taken by the `add` method. 

All three methods have been tested. `truncate` and `add` took less than 20 seconds to operate on a matrix with approximately 4.5 million non zero elements. 

**NOTE**: The following is a ballpark estimation, real world numbers may differ by a significant margin. 

The `smart` method was tested with a matrix containing roughly 4.5 million nonzero elements, and allowed to run for roughly five minutes. During that time, it completed 347104152 of 23240990033881 iterations required to finish the operation. Thus, it would take approximately 334784 minutes to complete the operation, or 5579 hours, or 232 days. This, the `smart` method is currently unsuitable for large matrices. 

Improving the speed of the `smart` method is currently considered low priority, as it's uses are fairly limited. 