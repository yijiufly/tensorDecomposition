from dexparser import Dexparser
from dexparser import uleb128_value
import disassembler
import numpy as np
from scipy import sparse
import sys

#dexfile = Dexparser('../apps/com.apporio.glitchr.apk_FILES/classes.dex')
dexfile = Dexparser(sys.argv[1])

opcode_list = []

c_list = dexfile.classdef_list()
class_cnt = 0
for class_idx, flag, superclass_idx, interfaces_off, source_file_idx, annotation_off, class_data_off, static_values_off in c_list:
	#print 'class: ' + str(class_cnt)
	class_cnt = class_cnt + 1
	if class_data_off == 0:
		continue

	[static_field_list, instance_field_list, direct_method_list, virtual_method_list] = dexfile.classdata_list(class_data_off)
	method_cnt = 0
	###compute 2-gram for direct method
	for diff, access_flags, code_off in direct_method_list:
		if code_off == 0:
			continue
		#print 'method: ' + str(method_cnt)
		size = ord(dexfile.mmap[code_off+12]) + (ord(dexfile.mmap[code_off+13])<<8) + (ord(dexfile.mmap[code_off+14])<<16) + (ord(dexfile.mmap[code_off+15])<<24)
		#print 'instr size:' + str(size)
		method_cnt += 1
		code_off += 16
		j = 0
		last_opc = -1
		temp_array = np.zeros(65536, int)
		while j in range(size * 2):
			opc = ord(dexfile.mmap[code_off + j])
			#print disassembler.opcode[opc]
			if j != 0:
				temp_array[last_opc * 256 + opc] += 1
			j += int(disassembler.length[opc])
			last_opc = opc
		opcode_list.append(temp_array.tolist())

	###compute 2-gram for virtual method
	for diff, access_flags, code_off in virtual_method_list:
		if code_off == 0:
			continue
		#print 'method: ' + str(method_cnt)
		size = ord(dexfile.mmap[code_off+12]) + (ord(dexfile.mmap[code_off+13])<<8) + (ord(dexfile.mmap[code_off+14])<<16) + (ord(dexfile.mmap[code_off+15])<<24)
		#print 'instr size:' + str(size)
		method_cnt += 1
		code_off += 16
		j = 0
		last_opc = -1
		temp_array = np.zeros(65536, int)
		while j in range(size * 2):
			opc = ord(dexfile.mmap[code_off + j])
			#print disassembler.opcode[opc]
			if j != 0:
				temp_array[last_opc * 256 + opc] += 1
			j += int(disassembler.length[opc])
			last_opc = opc
		opcode_list.append(temp_array.tolist())

#print opcode_list
mat = np.array(opcode_list)
sparse_mat = sparse.csr_matrix(mat)
print sparse_mat