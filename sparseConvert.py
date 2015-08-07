#!/usr/bin/python3


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

	