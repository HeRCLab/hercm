# Introduction
libSparseConvert contains two classes. `hercmio`, which does io for HeRCM files, and `sparseConvert`, which is a wrapper for `hercmio` and various scipy functions, as well as conversion between various matrix formats (currently HeRCM and mtx).

# Logging 
libSparseConvert uses `clogs.clogs` as a logger. `sparseConvert` and `hercmio` both contain instances of `clogs.clogs` as `this.logger`. Log contents can be accessed via the list of strings `INSTANCE.logger.contents`, and can be written via `INSTANCE.logger.log`, which takes one mandatory arguments, message, which contains the log message, and one optional argument, level, with is prefixed to the message (eg. `ERROR`). (note that level can be any string, it is simply for convenience) 

# Data structure reference 
## HeRCM dict
A dict containing a HeRCM file in coo format. An example follows. 

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

# Function reference 
## `hercmio`
`hercmio` takes one optional argument to `__init()__`, `logger`, which is an existing instance of `clogs.clogs`. If `logger` is not given, `hercmio` will create a new instance. 

### def read(this, filename):
* `filename` - string containing the file name or path to be opened 

Reads the given hercm file, verifies contents, then returns it. Returns None if an error is encountered. Return value is a HeRCM dict. 



### def generateVerificationSum(this,hercm):
* `hercm` - a HeRCM dict containing the matrix to analyze 

Generates and returns the verification sum (as specified in the [hercm spec](hercm-spec.md)) of the given matrix. If an error is encountered, returns None. 

### def verify(this, hercm):
* `hercm` - a HeRCM dict containing the matrix to verify

Returns True if the HeRCM is valid (based on the verification sum) and False if it is not. Returns None on error. 

### def write(this, hercm, filename):
* `hercm` - a HeRCM dict to write to the file
* `filename` - the string name or path of the file to write

Writes `hercm` as a HeRCM file to the given file. Also verifies the `hercm` against it's verification sum before writing. Returns True on success, and None on error. 


## `sparseConvert`
`sparseConvert` takes one optional argument to `__init()__`, `logger`, which is an existing instance of `clogs.clogs`. If `logger` is not given, `sparseConvert` will create a new instance.

### def readMatrix(this, filename, format):
* `filename` - string path or name of file to read
* `format` - string `mtx` or `hercmio` indicating the format of the matrix being read 

Reads the specified matrix into `this.HSM` (an instance of `libhsm.hsm`). Returns None on error, and True on success. Matrix which has been read my be accessed as a `libhsm.hsm` class instance via `this.HSM`. 

### def writeMatrix(this, filename, format):
* `filename` - string path or name of the file to write
* `format` - string format (`mtx` or `hercmio`) of the file to write 

Writes the contents of `this.HSM` to the given file with the given format. Returns True on success and None on failure. 

**ATTENTION**: Due to a bug in `scipy.io.mminfo.mmwrite`, symmetrical matrices written in mtx format will actually be written as asymmetrical. HeRCM matrices should not be affected. 





