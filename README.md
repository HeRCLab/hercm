# HeRCM 
HeRCM is a storage format for sparse matrices, origonally created for the HeRC research group at the University of South Carolina. The purpose of HeRCM is to provide a simple, easy to parse storage format as an alternative to matrix market or Harwell-Boeing. HeRCM files are rigid in structure, and while reference implementations are provided in C++98 and Python 3.4, io libraries should be trivial to implement in any language. 

The HeRCM spec can be viewed [here](hercm-spec.md).

# Tools 
Several tools are provided to make working with HeRCM easier, aside from the reference io libraries. 

## hercmExplorer 
Provides an interactive command shell for viewing and modifying any sparse matrix format supported by libSparseConvert. This is useful, because many sparse matrices are so large that directly viewing or editing their contents is impractical. 

## libSparseConvert 
A Python library for reading and writing sparse matrices in various formats, and permitting access to them in HeRCM format. 

## libhsm 
libhsm, short for lib HeRC Sparse Matrix, provides a Python class for HeRCM, permitting access in a variety of formats. 

## sparseConvet 
A wrapper and fronted for sparseConvert, created for the purpose of batch converting large volumes of files 
