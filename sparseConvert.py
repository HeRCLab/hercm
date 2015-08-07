#!/usr/bin/python3

"""
Copyright (c) 2015, Charles Daniels
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the 
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from 
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import libSparseConvert
import argparse
import pprint
pp = pprint.PrettyPrinter()


argparser = argparse.ArgumentParser(description="""utility to convert matrix 
market files to hercm and vice-versa""")

argparser.add_argument('-input','-i',
						nargs=1,
						required=True,
						help="""Specifies the path to the input matrix""")
argparser.add_argument('-output','-o',
						nargs=1,
						required=True,
						help="""Specifies the path of the output matrix""")
argparser.add_argument('-inputformat','-if',
						nargs =1, 
						required=True, 
						help="Specifies the format of the input matrix")
argparser.add_argument('-outputformat','-of',
						nargs=1,
						required=True,
						help="Specifies the format of the output matrix")
argparser.add_argument('--print','-p',
					   action='store_true',
					   default = False, 
					   help = """Print the matrix in human readable format 
before writing. Note that this is liable to cause excessive output on stdout, 
or out of memory errors""")

arguments = argparser.parse_args() 
inputFileName  = arguments.input[0]
outputFileName = arguments.output[0]
inputFormat    = arguments.inputformat[0]
outputFormat   = arguments.outputformat[0]
printMatrix = arguments.print 

supportedFormats = ['mtx','hercm']

if outputFormat not in supportedFormats:
	print("FATAL: output format {0} is unsupported".format(outputFormat))
	exit()
if inputFormat not in supportedFormats:
	print("FATAL: input format {1} is unsupported".format(inputFormat))
	exit()

SC = libSparseConvert.sparseConvert() 

if not SC.readMatrix(inputFileName, inputFormat):
	print("FATAL: libSparseConvert encountered an error. Log follows...")
	pp.pprint(SC.logger.contents)
	exit()
if not SC.writeMatrix(outputFileName, outputFormat):
	print("FATAL: libSparseConvert encountered an error. Log follows...")
	pp.pprint(SC.logger.contents)
	exit()


if printMatrix:
	print(SC.HSM.getInFormat('coo').todense())

	