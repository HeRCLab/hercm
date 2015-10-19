# HeRC Matrix Tools (HeRCM)

# Introduction
**ATTENTION**: This project is still under active development. While most of the code has been tested for basic functionality, performance and edge cases have not been evaluated yet. 

HeRC Matrix Tools is a collection of open source sparse and symmetric matrix tools, originally created for the University of South Carolina HeRC research group. 

# Tools
## Better Matrix Format (BXF)
Better Matrix Format (previously called "HeRCM format", with the `.hercm` file extension) is a simple matrix storage format, which stores COO-compressed sparse matrices in a human-readable and writable format. BXF tries to avoid unneeded complexity by utilizing a simple, rigid file format.

For more information, review the [bxf specification](doc/bxf-sepec.md). 

## BXFExplorer
BXFExplorer is a tool which can be used for interacting with sparse matrix files. It can read and write matrices in a variety of formats, including `.bxf`, `.mtx`, and `.mat` formats. 

For more information, review the [BXFExplorer documentation](doc/bxf-explorer.md)