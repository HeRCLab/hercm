# Introduction 
sparseConvert is a utility for converting between matrix file formats supported by libSparseConvert. 

# Installation
Move `sparseConvert.py`, `libSparseConvert.py`, `libhsm.py`, and `cogs.py` into the same directory which is in your `$PATH`, or just run `sparseConvert.py` directly. 

# Usage
```
usage: sparseConvert.py [-h] -input INPUT -output OUTPUT -inputformat
                        INPUTFORMAT -outputformat OUTPUTFORMAT [--print]
                        [--noworkaround]

utility to convert matrix market files to hercm and vice-versa

optional arguments:
  -h, --help            show this help message and exit
  -input INPUT, -i INPUT
                        Specifies the path to the input matrix
  -output OUTPUT, -o OUTPUT
                        Specifies the path of the output matrix
  -inputformat INPUTFORMAT, -if INPUTFORMAT
                        Specifies the format of the input matrix
  -outputformat OUTPUTFORMAT, -of OUTPUTFORMAT
                        Specifies the format of the output matrix
  --print, -p           Print the matrix in human readable format before
                        writing. Note that this is liable to cause excessive
                        output on stdout, or out of memory errors
  --noworkaround, --n   Do not use a workaround to fix mtx files. If
                        specified, all mtx files will be asymmetric,
                        regardless of matrix symmetry.

```

# Workaround for issue #1 
As a workaround for scipy not writing symmetric matrices to mtx correctly, an additional script will automatically be run on the output matrix, to put it in symmetrical form. If you do not wish to use this workaround, you can use the `--n` flag. 