#!/usr/bin/python3


import libSparseConvert
import argparse
import pprint
pp = pprint.PrettyPrinter()
import os 


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
argparser.add_argument('--noworkaround','--n',
						action='store_true',
						help="""Do not use a workaround to fix mtx files. If 
specified, all mtx files will be asymmetric, regardless of matrix symmetry. """)

arguments = argparser.parse_args() 
inputFileName  = arguments.input[0]
outputFileName = arguments.output[0]
inputFormat    = arguments.inputformat[0]
outputFormat   = arguments.outputformat[0]
printMatrix	   = arguments.print 
noworkaround   = arguments.noworkaround

supportedFormats = ['mtx','hercm']

if outputFormat not in supportedFormats:
	print("FATAL: output format {0} is unsupported".format(outputFormat))
	exit()
if inputFormat not in supportedFormats:
	print("FATAL: input format {0} is unsupported".format(inputFormat))
	exit()

SC = libSparseConvert.sparseConvert() 

print("reading matrix...")
SC.readMatrix(inputFileName, inputFormat)

print("writing matrix...")
SC.writeMatrix(outputFileName, outputFormat)



if printMatrix:
	print(SC.HSM.getInFormat('coo').todense())

if outputFormat == 'mtx':
	if SC.HSM.symmetry == 'SYM':
		print("WARNING: output format is MTX, but symmetry is symmetric") 
		if noworkaround:
			print("--noworkaround given, not repairing matrix")
		else:
			os.system("python generate_symmetric_matrices.py {0}"
					  .format(outputFileName))
			os.remove(outputFileName)
			os.remove(outputFileName+'.pvalcol')
			os.rename(outputFileName+".pmtx", outputFileName)



	