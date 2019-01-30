from Crypto.Cipher import AES
from os import urandom
from base64 import b64encode
key = urandom(16)
from challenge53 import iteratedHash

def find_2_hash_collision(H1,H2,length):
	hash_1_value = []
	M_1_value = []

	for i in range(2**(length/2)):
		M = urandom(length)
		hash_1_value.append(iteratedHash(M,H1,length))
		M_1_value.append(M)
	while True:
		M = urandom(length)
		hash2 = iteratedHash(M,H2,length)
		if hash2 in hash_1_value:
			for i in range(len(hash_1_value)):
				if hash2 == hash_1_value[i]:
					return (M_1_value[i],M,hash2)

def buildDiamondStructure (k):
	Value_structure = []
	DiamondStructure = []
	Value_structure_layer = []
	DiamondStructure_layer = []
	for i in range(2**k):
		DiamondStructure_layer.append(urandom(length))
		if i % 2 == 1 :
			Value_structure_layer.append((DiamondStructure_layer[-
				2],DiamondStructure_layer[-1]))
	DiamondStructure.append(DiamondStructure_layer)
	Value_structure.append(Value_structure_layer)
	for i in range(k,1,-1):
		DiamondStructure_layer_new = []
		Value_structure_layer_new = []
		for i in range(2 ** (k-1)):
			H1 = DiamondStructure_layer[2*i]
			H2 = DiamondStructure_layer[2*i+1]
			leaf = find_2_hash_collision(H1,H2,length)
			DiamondStructure_layer_new.append(leaf[2])
			Value_structure_layer_new.append((leaf[0],leaf[1]))
		DiamondStructure_layer = DiamondStructure_layer_new
		Value_structure_layer = Value_structure_layer_new
		DiamondStructure.append(DiamondStructure_layer)
		Value_structure.append(Value_structure_layer)
	return (DiamondStructure,Value_structure)

def followTheLeaf (layer,position):
	suffix = ""
	while True:
		position = position / 2
		layer += 1
		suffix += Value_structure[layer][position]
		if position == 0 :
			break
	return suffix