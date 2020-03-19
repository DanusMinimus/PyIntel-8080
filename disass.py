import bitstring as bitstr

instruction_set =  {
	"01DDDSSS":"MOV",
	"00DDD110":"MVI!", 
	"00RP0001":"LXI#", 
	"00111010":"LDA#",
	"00110010":"STA#",
	"00101010":"LHLD#", 
	"00100010":"SHLD#", 
	"00RS1010":"LDAX", 
	"00RS0010":"STAX",
	"11101011":"XCHG", 
	"10000SSS":"ADD", 
	"11000110":"ADI!", 
	"10001SSS":"ADC", 
	"11001110":"ACI!",
	"10010SSS":"SUB", 
	"11010110":"SUI!", 
	"10011SSS":"SBB",
	"11011110":"SBI!", 
	"00DDD100":"INR", 
	"00DDD101":"DCR", 
	"00RP0011":"INX", 
	"00RP1011":"DCX", 
	"00RP1001":"DAD", 
	"00100111":"DAA", 
	"10100SSS":"ANA", 
	"11100110":"ANI!", 
	"10110SSS":"ORA",
	"11110110":"ORI!", 
	"10101SSS":"XRA",
	"11101110":"XRI!", 
	"10111SSS":"CMP", 
	"11111110":"CPI!",
	"00000111":"RLC",
	"00001111":"RRC", 
	"00010111":"RAL",
	"00011111":"RAR",
	"00101111":"CMA", 
	"00111111":"CMC", 
	"00110111":"STC",
	"11000011":"JMP#" ,
	"11CCC010":"Jccc#", 
	"11001101":"CALL#", 
	"11CCC100":"Cccc#", 
	"11001001":"RET", 
	"11CCC000":"Rccc", 
	"11NNN111":"RST", 
	"11101001":"PCHL", 
	"11ST0101":"PUSH", 
	"11ST0001":"POP",
	"11100011":"XTHL",
	"11111001":"SPHL",
	"11011011":"IN!", 
	"11010011":"OUT!", 
	"11111011":"EI", 
	"11110011":"DI", 
	"01110110":"HLT",
	"00000000":"NOP",
	"00010000":"NOP",
	"00100000":"NOP",
	"00110000":"NOP",
	"00001000":"NOP",
	"00011000":"NOP",
	"00101000":"NOP",
	"00111000":"NOP"

}

register_encoding = {
	"111":"A",
	"000":"B",
	"001":"C",
	"010":"D",
	"011":"E",
	"100":"H",
	"101":"L",
	"110":"M"
}

register_pair = {
	"00":"B",
	"01":"D",
	"10":"H",
	"11":"SP"
}

register_special = {
	"00":"B",
	"01":"D",
}

register_stack = {
	"00":"B",
	"01":"D",
	"10":"H",
	"11":"PSW"
}

pre_def = {
	"000":"0x0",
	"001":"0x8",
	"010":"0x10",
	"011":"0x18",
	"100":"0x20",
	"101":"0x28",
	"110":"0x30",
	"111":"0x38"

}

condition_code = {
	"000":"NZ",
	"001":"Z",
	"010":"NC",
	"011":"C",
	"100":"PO",
	"101":"PE",
	"110":"P",
	"111":"M"
}

#IN - Basic instruction set with replacable characters
#OUT - Newly generated instruction set containing all possible combinations of opcodes
def generateDynamic(instr_set):

	instruction_set_gen = {}

	for k, v in instr_set.items():

		string_new = str(k)

		if "SSS" in string_new:

			for source in register_encoding:

				INSTR = string_new.replace("SSS", source)

				if "DDD" in k:
					for dest in register_encoding:

						MOV = INSTR.replace("DDD", dest)
						instruction_set_gen[MOV] = str(v) + " " + register_encoding.get(dest) + " " +  register_encoding.get(source)
				else:
					instruction_set_gen[INSTR] = str(v) + " " + register_encoding.get(source)

			continue

		if "DDD" in string_new:
			for dest in register_encoding:
				INSTR = string_new.replace("DDD", dest)
				instruction_set_gen[INSTR] = str(v) + " " + register_encoding.get(dest)
			continue

		if "RP" in string_new:
			for rp in register_pair:
				INSTR = string_new.replace("RP", rp)
				instruction_set_gen[INSTR] = str(v) + " " + register_pair.get(rp)
			continue

		if "RS" in string_new:
			for rp in register_special:
				INSTR = string_new.replace("RS", rp)
				instruction_set_gen[INSTR] = str(v) + " " + register_special.get(rp)

		if "ST" in string_new:
			for rp in register_stack:
				INSTR = string_new.replace("ST", rp)
				instruction_set_gen[INSTR] = str(v) + " " + register_stack.get(rp)

		if "NNN" in string_new:
			for predef in pre_def:
				INSTR = string_new.replace("NNN", predef)
				instruction_set_gen[INSTR] = str(v) + " " + pre_def.get(predef)
			continue

		if "CCC" in string_new:
			for ccc in condition_code:
				INSTR = string_new.replace("CCC", ccc)
				instruction_set_gen[INSTR] = (str(v)  + condition_code.get(ccc)).replace("ccc", "")
			continue

		instruction_set_gen[string_new] = (str(v))		
	return instruction_set_gen

#[---Generated instruction set---]#
instruction_set_8080 = generateDynamic(instruction_set)

#Loads invaders file and returns its memory contents
def returnMemory(str_filename , im_org = 0):
	memory = []
	if(im_org != 0):
		memory.extend([0] * (im_org))

	with open(str_filename, 'rb') as f:
		byte = f.read(1)

		while byte:
			memory.append(ord(byte))
			byte = f.read(1)

	memory.extend([0]*(0x10000 - len(memory)))
	return memory

#IN - Memory map
#OUT - Prints out memory list
def printMemoryMap(memory):
	k = 0
	for v in memory:
		if k  % 8 != 0:
			print("[" + format(v, 'x').zfill(2) + "]", end = '')
		else:
			print("")
		k = k + 1

#IN - Memory map
#IN - Program counter
#OUT - Parsed instruction from memory
def parseInstruction(memory, pc):
	byte = memory[pc]
	bitstr_current = bitstr.BitStream(hex(byte))
	opcode = format(byte, 'x')

	str_instruction = instruction_set_8080.get(bitstr_current.bin.zfill(8), 'None')

	if(str_instruction is None):
		print("OPCODE: " + bitstr_current.bin.zfill(8))
		for k, v in instruction_set_8080.items():
			if(k in "LXI"):
				print(v)

	if "!" in str_instruction:
		pc = pc + 1
		hblb = memory[pc]

		str_instruction = str_instruction.replace("!", "") + " " + str(hblb)
		opcode = opcode + format(hblb, 'x')

	if "#" in str_instruction:
		pc = pc + 1
		byte = memory[pc]
		lb = int(byte) & 0xff

		pc = pc + 1
		byte = memory[pc]
		hb = int(byte) & 0xff

		hblb = str(((hb << 8) | lb))

		str_instruction = str_instruction.replace("#", "") + " " + hblb
		opcode = opcode + format(int(lb), 'x').zfill(2) + format(int(hb), 'x').zfill(2)


	return str_instruction, opcode, pc


def printInstruction(str_instruction):
	str_split = str_instruction.split(" ")

	if(len(str_split) == 2):
		if(str_split[1].isdigit()):
			str_split[1] = format(int(str_split[1]), 'x').zfill(4)
		return str_split[0] + " " + str_split[1]

	if(len(str_split) == 3):
		if(str_split[2].isdigit()):
			str_split[2] = format(int(str_split[2]), 'x').zfill(4)

		return str_split[0] + " " + str_split[1] + ", " + str_split[2]

	return str_split[0]

"""
Inst      Encoding        
--------------------------
MOV D,S   01DDDSSS        
MVI D,#   00DDD110 db     
LXI RP,#  00RP0001 lb hb  
LDA a     00111010 lb hb  
STA a     00110010 lb hb  
LHLD a    00101010 lb hb  
SHLD a    00100010 lb hb  
LDAX RP   00RP1010 *1     
STAX RP   00RP0010 *1     
XCHG      11101011        
ADD S     10000SSS        
ADI #     11000110 db     
ADC S     10001SSS        
ACI #     11001110 db     
SUB S     10010SSS        
SUI #     11010110 db     
SBB S     10011SSS        
SBI #     11011110 db     
INR D     00DDD100        
DCR D     00DDD101        
INX RP    00RP0011        
DCX RP    00RP1011        
DAD RP    00RP1001        
DAA       00100111        
ANA S     10100SSS        
ANI #     11100110 db     
ORA S     10110SSS        
ORI #     11110110        
XRA S     10101SSS        
XRI #     11101110 db     
CMP S     10111SSS        
CPI #     11111110        
RLC       00000111        
RRC       00001111        
RAL       00010111        
RAR       00011111        
CMA       00101111        
CMC       00111111        
STC       00110111        
JMP a     11000011 lb hb  
Jccc a    11CCC010 lb hb  
CALL a    11001101 lb hb  
Cccc a    11CCC100 lb hb  
RET       11001001        
Rccc      11CCC000        
RST n     11NNN111        
PCHL      11101001        
PUSH RP   11RP0101 *2     
POP RP    11RP0001 *2     
XTHL      11100011        
SPHL      11111001        
IN p      11011011 pa     
OUT p     11010011 pa     
EI        11111011        
DI        11110011        
HLT       01110110        
NOP       00000000        

CONSTANT INSTRUCTION ----- """
