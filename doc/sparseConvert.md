# Introduction 
sparseConvert is a utility for converting between matrix file formats supported by libSparseConvert. 

# Installation
Move `sparseConvert.py`, `libSparseConvert.py`, `libhsm.py`, and `cogs.py` into the same directory which is in your `$PATH`, or just run `sparseConvert.py` directly. 

# Usage
```
usage: sparseConvert.py [-h] [-mtx MTX] [-output OUTPUT] [-hercm HERCM]
                        [--print]

utility to convert matrix market files to hercm and vice-versa

optional arguments:
  -h, --help            show this help message and exit
  -mtx MTX, -m MTX      specifies the path to the mtx file to read, converts
                        it to hercm, then writes it out with the same name and
                        the hermc extension
  -output OUTPUT, -o OUTPUT
                        specifies the output file for either -mtx or -hercm;
                        overrides the generated file names for either option
  -hercm HERCM, -e HERCM
                        specifies the path of the hercm file to be read,
                        converts it to hercm, then writes it out with the same
                        name and the mtx extension
  --print, -p           Print the matrix in human readable format before
                        writing. Note that this is liable to cause excessive
                        output on stdout, or out of memory errors
```