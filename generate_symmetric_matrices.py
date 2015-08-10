"""
Copyright (c) 2015, Steve Rubin

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of {{ project }} nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import pdb
import os
import sys
import numpy as np

#in the MTX: #rows, #cols, #nnz
#in the MTX: row, col, val
#pdb.set_trace()
if(len(sys.argv) != 2):
	print "ERROR: Please specify the matrix filename"
	#print str(sys.argv[0])
	sys.exit()

def check_for_comments(lines_list):
	number_of_comment_lines = 0
	
	new_line = matrix_list[number_of_comment_lines]
	
	while(new_line.find("%") != -1):
		number_of_comment_lines += 1
		new_line = matrix_list[number_of_comment_lines]
	return number_of_comment_lines


matrix_file = open(sys.argv[1], "r")

#read all the lines of a file in a string.
matrix_string = matrix_file.read()
matrix_file.close()

#read all the lines of a file in a list.
matrix_file = open(sys.argv[1], "r")
matrix_list = matrix_file.readlines()
matrix_file.close()
#print kernel_string


print ""



number_of_comment_lines = check_for_comments(matrix_list)
if (number_of_comment_lines != 0 ):
	print "found " + str(number_of_comment_lines) + " lines of comments"



for x in range(0, number_of_comment_lines):
	del matrix_list[0]
	print "deleting line #" + str(x) + " as it is a comment"

#for i in matrix_list:
#	print i

matrix_numbers_list = []
for i in range(0, len(matrix_list)):
	matrix_numbers_list.append(matrix_list[i].split())

#for i in matrix_numbers_list:
#	print i

#print str(len(matrix_numbers_list))
#delete empty first and last elements of the list
#del matrix_numbers_list[0]
#del matrix_numbers_list[len(matrix_numbers_list) - 1]

#if the number of elements in the list is 3 - row, col, val
if(len(matrix_numbers_list[1]) == 3):
	print "the mtx file contains non binary values"
	for i in range(0, len(matrix_numbers_list)):
		matrix_numbers_list[i][0] = int(matrix_numbers_list[i][0])
		matrix_numbers_list[i][1] = int(matrix_numbers_list[i][1])
		matrix_numbers_list[i][2] = float(matrix_numbers_list[i][2])
else:
#if the number of elements in the list is 2 - row, col, 1
	print "the mtx file contains binary values"
	for i in range(0, len(matrix_numbers_list)):
		matrix_numbers_list[i][0] = int(matrix_numbers_list[i][0])
		matrix_numbers_list[i][1] = int(matrix_numbers_list[i][1])
		matrix_numbers_list[i].append(float(1))

#matrix_numbers_list = [int(i) for i in results]

print ""
number_of_rows_cols_nnz = matrix_numbers_list[0]
del matrix_numbers_list[0]
number_of_rows = number_of_rows_cols_nnz[0]
number_of_cols = number_of_rows_cols_nnz[1]
number_of_nnz = int(number_of_rows_cols_nnz[2])
print "#rows - " + str(number_of_rows)
print "#cols - " + str(number_of_cols)
print "#nnz - " + str(number_of_nnz)

##AT THIS POINT we have matrix_numbers_list which is  a list of lists each of them is one element in mtx file
##AT THIS POINT we have number_of_rows_cols_nnz

print ""
list_to_delete = []
number_of_nnz_deleted = 0
for i in range(0, len(matrix_numbers_list)):
	#print i
	if(matrix_numbers_list[i][2] == 0):
		list_to_delete.append(i)
		
		
for i in range(0, len(list_to_delete)):
	print "deleting " + str(matrix_numbers_list[list_to_delete[i]]) + " as the value is zero"
	del matrix_numbers_list[list_to_delete[i]]
	number_of_nnz_deleted += 1 

		
		
print ""
#for i in matrix_numbers_list:
#	print i
	
list_to_delete = []

##AT THIS POINT we have matrix_numbers_lista with no 0 elements
for i in range(0, len(matrix_numbers_list)):
	#print i
	element_column = matrix_numbers_list[i][1]
	element_row = matrix_numbers_list[i][0]
	element_value = matrix_numbers_list[i][2]
	for j in range ((i+1), len(matrix_numbers_list)):
		if(matrix_numbers_list[j][1] == element_row and matrix_numbers_list[j][0] == element_column 
			and matrix_numbers_list[j][2] == element_value):
			list_to_delete.append(j)
			
	
print ""
#ERROR HERE: with indexes
for i in range(0, len(list_to_delete)):
	try:
		print "deleting " + str(matrix_numbers_list[list_to_delete[i]]) + " as the value has a duplicate"
		del matrix_numbers_list[list_to_delete[i]]
		number_of_nnz_deleted += 1 
	except IndexError:
		print("ERROR: cannot access index {0} of matrix with {1} elements"
			  .format(i, len(matrix_numbers_list)))
		print(matrix_numbers_list)

number_of_nnz = number_of_nnz - number_of_nnz_deleted

print ""
#print "#rows - " + str(number_of_rows)
#print "#cols - " + str(number_of_cols)
#print "#nnz - " + str(number_of_nnz)
#print ""

for i in matrix_numbers_list:
	if (i[0] > i[1]):
		print "found an element in the bottom triangle " + str(i) + " moving him to top"
		temp = i[0]
		i[0] = i[1]
		i[1] = temp

##AT THIS POINT we have matrix_numbers_list with no 0 elements, no duplicate elements, no elements in the botton triangle

for i in range(0, len(matrix_numbers_list)):
	matrix_numbers_list[i] = tuple(matrix_numbers_list[i])

#print matrix_numbers_list	
data_type = [('row', int), ('col', int), ('val', float)]
#data_type = 'i4, i4, f4'
np_matrix_numbers_list =  np.array(matrix_numbers_list, dtype = data_type)
#print np_matrix_numbers_list


sorted_matrix = np.sort(np_matrix_numbers_list, order=["row", "col"])
print ""
#print sorted_matrix

##AT THIS POINT we have sorted_matrix with no 0 elements, no duplicate elements, sorted by row first col second, no elements in the bottom triangle
## export ti .mtx file
new_mtx_file_name = str(sys.argv[1]) + ".pmtx"
new_mtx_file = open(new_mtx_file_name, "w")
new_mtx_file.write(str(number_of_rows_cols_nnz[0]) + " " + str(number_of_rows_cols_nnz[1]) + " " + str(int(number_of_rows_cols_nnz[2])))
new_mtx_file.write("\n")

ptr = []
#ptr.extend([0])
ptr_counter = 0
for i in sorted_matrix:
	new_mtx_file.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]))
	new_mtx_file.write("\n")
	if (ptr_counter + 1 == i[0]):
		ptr_counter += 1
		itemindex = np.where(sorted_matrix==i)
		ptr.append(itemindex[0])
		#

ptr.append([number_of_nnz])
new_mtx_file.close()

## export ti .valcol file
new_valcol_file_name = str(sys.argv[1]) + ".pvalcol"
new_valcol_file = open(new_valcol_file_name, "w")

new_valcol_file.write(str(number_of_rows) + " " + str(number_of_nnz))
new_valcol_file.write("\n")

#create ptr array for the valcol file
for i in sorted_matrix:
	new_valcol_file.write(str(i[2]) + " " + str(i[1]))
	new_valcol_file.write("\n")
	

for i in ptr:
	new_valcol_file.write(str(i[0]))
	new_valcol_file.write("\n")

new_valcol_file.close()

print "		!SUCCESS!"
print "		please check synsymmetric matrices: " + new_mtx_file_name + " and " + new_valcol_file_name
print ""

