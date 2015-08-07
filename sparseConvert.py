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

argparser.add_argument('-mtx','-m',
						nargs=1,
						default=[None],
						help="""specifies the path to the mtx file to read,
converts it to hercm, then writes it out with the same name and the hermc 
extension""")
argparser.add_argument('-output','-o',
						nargs=1,
						default=[None],
						help="""specifies the output file for either -mtx or
-hercm; overrides the generated file names for either option""")
argparser.add_argument('-hercm','-e',
						nargs=1,
						default=[None],
						help="""specifies the path of the hercm file to be read,
converts it to hercm, then writes it out with the same name and the mtx
extension """)
argparser.add_argument('--print','-p',
					   action='store_true',
					   default = False, 
					   help = """Print the matrix in human readable format 
before writing. Note that this is liable to cause excessive output on stdout, 
or out of memory errors""")

arguments = argparser.parse_args() 
mtxFileName = arguments.mtx[0]
hercmFileName = arguments.hercm[0]
outputFileName = arguments.output[0] 
printMatrix = arguments.print 

if mtxFileName == None and hercmFileName == None:
	print("FATAL: an input file must be specified")
	exit()
if mtxFileName != None and hercmFileName != None:
	print("FATAL: exactly one input file must be specified")
	exit()

if outputFileName == None:
	if mtxFileName != None: 
		outputFileName = mtxFileName[:-3] + "hercm"
	else:
		outputFileName = hercmFileName[:-4] + "mtx"

SC = libSparseConvert.sparseConvert() 

if mtxFileName != None: 
	if not SC.readMatrix(mtxFileName,'mtx'):
		print("FATAL: libSparseConvert encountered an error, here is the log:")
		pp.pprint(SC.logger.contents)
		exit()

	if not SC.writeMatrix(outputFileName,'hercm'):
		print("FATAL: libSparseConvert encountered an error, here is the log:")
		pp.pprint(SC.logger.contents)
		exit()

if hercmFileName != None:
	if not SC.readMatrix(hercmFileName,'hercm'):
		print("FATAL: libSparseConvert encountered an error, here is the log:")
		pp.pprint(SC.logger.contents)
		exit()

	if not SC.writeMatrix(outputFileName, 'mtx'):
		print("FATAL: libSparseConvert encountered an error, here is the log:")
		pp.pprint(SC.logger.contents)
		exit()

if printMatrix:
	print(SC.HSM.getInFormat('coo').todense())

	