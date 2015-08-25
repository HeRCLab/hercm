import sys, traceback, pickle 
import numpy
sys.path.append('..')

print("HeRCm unit tests beginning...") 

### unit tests ###
# libhsm (import)
# libhsm.hsm.getInFormat 
# libhsm.hsm.addElement 
# libhsm.hsm.getElement 
# libhsm.hsm.castElement 
# libhsm.hsm.searchElement 
# libhsm.hsm.removeElement 
# libhsm.hsm.getValue 
# libhsm.hsm.setValue 
# libhsm.hsm.removeZeros 
# libhsm.hsm.replaceContents 
# libhsm.hsm.checkSymmetry 
# libhsm.hsm.makeSymmetrical 
# libhsm.hsm.makeAsymmetrical 
# libhsm.hsm.makeRowMajor 

# libSparseConvert (import) 
# hercmio.read
# hercmio.generateVerificatonSum 
# hercmio.verify
# hercmio.write
# sparseConvert.readMatrix
# sparseConvert.writeMatrix 

tests = {"libhsm"				:False,
'libhsm.hsm'					:False,
"libhsm.hsm.getInFormat"		:False,
"libhsm.hsm.addElement"			:False,
"libhsm.hsm.getElement"			:False,
"libhsm.hsm.castElement"		:False,
"libhsm.hsm.searchElement"		:False,
"libhsm.hsm.removeElement"		:False,
"libhsm.hsm.getValue"			:False,
"libhsm.hsm.setValue"			:False,
"libhsm.hsm.removeZeros"		:False,
"libhsm.hsm.replaceContents"	:False,
"libhsm.hsm.checkSymmetry"		:False,
"libhsm.hsm.makeSymmetrical"	:False,
"libhsm.hsm.makeAsymmetrical"	:False,
"libhsm.hsm.makeRowMajor"	 	:False,
"libSparseConvert"	 			:False,
"hercmio.read"				 	:False,
"hercmio.generateVerificatonSum":False,
"hercmio.verify"				:False,
"hercmio.write"					:False,
"sparseConvert.readMatrix"		:False,
"sparseConvert.writeMatrix"		:False
}

# libhsm 
print("testing libhsm... ",end='')
try:
	import libhsm
	print("OK")
	tests['libhsm'] = True 
except Exception as e: 
	print("FAILED")
	print('-'*20,'traceback','-'*20)
	traceback.print_exc(file=sys.stdout)
	tests['libhsm'] = False

print("instantiating libhsm.hsm instance... ",end='')
try:
	HSM = libhsm.hsm()
	print("OK")
	tests['libhsm.hsm'] = True
except Exception as e: 
	print("FAILED")
	print('-'*20,'traceback','-'*20)
	traceback.print_exc(file=sys.stdout)
	tests['libhsm.hsm'] = False 

print("loading dummy HSM instance... ",end='')
dummyHSM = pickle.load(open("bcspwr01_HSM.p",'rb'))
print("done")  

print("loading test data... " , end='')
dummyCOO = pickle.load(open("bcspwr01_COO.p",'rb'))
print("done") 

# libhsm.getInFormat
print("testing libhsm.hsm.getInFormat... ", end='') 
try:
	if not (numpy.allclose(dummyHSM.getInFormat('coo').toarray(),
						   dummyCOO.toarray())):
		print("FAILED")
		print("data returned by getInFormat doe snot match tests data!")
		tests['libhsm.hsm.getInFormat'] = False 
	else: 
		print("OK")
		tests['libhsm.hsm.getInFormat'] = True 
except Exception as e:
	print("FAILED")
	print('-'*20,'traceback','-'*20)
	traceback.print_exc(file=sys.stdout)
	tests['libhsm.hsm.getInFormat'] = False  



