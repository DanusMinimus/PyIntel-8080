import disass as dislib
import cpulib
import sys
import screenlib

class Core(object):

    def __init__(self):

        self.im_org = 0x0
        self.list_memory = dislib.returnMemory("invaders", self.im_org)
        self.screen = screenlib.Screen()
        """self.list_memory[1436] = 195
        self.list_memory[1437] = 240
        self.list_memory[1438] = 5"""

        self.advance = 1

        self.condition_bits = {
            "C":0,
            "1":1,
            "P":0,
            "0":0,
            "A":0,
            "5":0,
            "Z":0,
            "S":0,
        }

        self.register_encoding = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "H": 0,
            "L": 0,
            "FLAGS": 2
        }

        self.register_pair = {
            "B": "C",
            "D": "E",
            "H": "L",
            "PSW": "FLAGS",
            "SP": 0,
            "PC": self.im_org,
            "BP1": 0,
            "BP2": 0,
            "BP3": 0
        }

    def stringFlags(self):
        str_flags = "CPAZS"
        for k, v in self.condition_bits.items():
            index = str_flags.find(k)
            if(v == 0 and index != -1):
                str_flags = str_flags.replace(k, '.')

        return str_flags
                
    def printCPUState(self):

        print("[---Flags---]")
        for k, v in self.condition_bits.items():
            print(k + ": " + str(v))

        print("-------------------------")

        #Implement stack print
        sp = self.register_pair["SP"]
        print("[---Stack---]")
        for k in range(sp + 4, sp - 20, -2):
            print("[0x" + format(k, 'x').zfill(4) + "]" + ": 0x" + format(self.list_memory[k+1], 'x').zfill(2) + format(self.list_memory[k], 'x').zfill(2), end = '')
            if(k == sp):
                print(" <---[sp]")
            else:
                print("")
        print("-------------------------")


        print("[---Registers---]")
        for k, v in self.register_encoding.items():
            print(k + ": 0x" + format(v, 'x').zfill(2))


        print("-------------------------")

        print("[---Register Pair---]")
        for k, v in self.register_pair.items():
            im_a = self.getPairFull(k)
            print(k + ": 0x" + format(im_a, 'x').zfill(4))

        print("-------------------------")

        pc = self.register_pair["PC"]
        for k in range(pc , pc + 20):
            str_instruction, opcode, next_pc = dislib.parseInstruction(self.list_memory, pc)
            str_printInstruction = dislib.printInstruction(str_instruction)

            print("[0x" + format(pc, 'x').zfill(4) + "]" + ": " + opcode.ljust(10) + str_printInstruction, end = '')
            if(k == self.register_pair["PC"]):
                print(" <---[pc] \t" + self.stringFlags())
            else:
                print("")

            pc = next_pc + 1

        print("-------------------------")


    def printInstructions(self, number_amount = 10):
        pc = self.register_pair["PC"]
        for k in range(pc , pc + number_amount):
            str_instruction, opcode, next_pc = dislib.parseInstruction(self.list_memory, pc)
            str_printInstruction = dislib.printInstruction(str_instruction)

            print("[0x" + format(pc, 'x').zfill(4) + "]" + ": " + opcode.ljust(10) + str_printInstruction, end = '')
            if(k == self.register_pair["PC"]):
                print(" <---[pc] \t" + self.stringFlags())
            else:
                print("")

            pc = next_pc + 1

        print("-------------------------")

    def getNewFlagReg(self):

        flags = [0,0,0,0,0,0,0,0]
        itr = 7
        for k, v in self.condition_bits.items():
            flags[itr] = v
            itr = itr - 1

        flags = int("".join(map(str, flags)), 2) 

        return flags




    def setFlags(self, reg_a, noFlag = ""):

        if(type(reg_a) is str):
            im_res = self.getReg("A") & 511
        else:
            im_res = reg_a & 511

        if("TC" != noFlag):
            self.condition_bits["C"] = (im_res >> 8) & 1

        im_res = im_res & 255

        if("FC" != noFlag): 
            if(0 == format(im_res, "b").count('1') % 2):
                self.condition_bits["P"] = 1
            else:
                self.condition_bits["P"] = 0

            if(0 != (im_res)):
                self.condition_bits["Z"] = 0
            else:
                self.condition_bits["Z"] = 1

            if(im_res >> 7 == 1):
                self.condition_bits["S"] = 1
            else:
                self.condition_bits["S"] = 0 

        if(type(reg_a) is str):     
            self.register_encoding[reg_a] = im_res & 255
        self.register_encoding["FLAGS"] = self.getNewFlagReg()


    def setImPair(self, im_a, im_b):

        im_a = im_a & 255
        im_b = im_b & 255

        im_full = (im_a << 8) | im_b

        return im_full

    def getImPair(self, im_all):

        return (im_all >> 8) & 255, im_all & 255

    def getPair(self, reg_a):

        if("SP" == reg_a or "PC" == reg_a or "BP" in reg_a):
            return (self.register_pair[reg_a] >> 8) & 255, self.register_pair[reg_a] & 255

        if("PSW" == reg_a):
            flags = self.getNewFlagReg()
            self.register_encoding["FLAGS"] = flags
            return self.register_encoding["A"], self.register_encoding["FLAGS"]

        reg_b = self.register_pair[reg_a]

        return self.register_encoding[reg_a], self.register_encoding[reg_b]

    def setPair(self, reg_a, im_a, im_b):

        im_a = im_a & 255
        im_b = im_b & 255

        if("SP" == reg_a or "PC" == reg_a or "BP" in reg_a):
            new_im = (im_a << 8) | im_b
            self.register_pair[reg_a] = new_im
            return 0

        elif("PSW" == reg_a):

            reg_a = "A"
            reg_b = "FLAGS"
            flags_str = format(im_b, 'b').zfill(8)
            itr = 7

            for k, v in self.condition_bits.items():
                self.condition_bits[k] = int(flags_str[itr])
                itr = itr - 1

        else:
            reg_b = self.register_pair[reg_a]

        self.register_encoding[reg_a] = im_a
        self.register_encoding[reg_b] = im_b
        return 1


    def getPairFull(self, reg_a):
        im_high, im_low = self.getPair(reg_a)
        im_full = self.setImPair(im_high, im_low)
        return im_full

    def setPairFull(self, reg_a, im_full):
        im_high, im_low = self.getImPair(im_full)
        self.setPair(reg_a, im_high, im_low)

    def setMemory(self, im_addr, im_a):
        self.list_memory[im_addr] = im_a

    def getMemory(self, im_addr):
        return self.list_memory[im_addr]

    def setReg(self, reg_a, im_a):
        im_a = im_a & 255
        if("M" == reg_a):
            im_full = self.getPairFull("H")
            self.setMemory(im_full, im_a)
        else:
            self.register_encoding[reg_a] = im_a

    def getReg(self, reg_a):
        if("M" == reg_a):
            im_full = self.getPairFull("H")
            return self.getMemory(im_full)
        else:
            return self.register_encoding[reg_a]

    def setBP(self, reg_a, im_a):
        self.setPairFull(reg_a, im_a)

    def CPUJumpTable(self, str_instruction):

        str_split = str_instruction.split(" ")

        im_pc = self.getPairFull("PC")

        if(len(str_split) > 1 and str_split[1].isdigit()):
            str_split[1] = int(str_split[1]) 

        if(len(str_split) > 2 and str_split[2].isdigit()):
            str_split[2] = int(str_split[2])

        if(None == str_split[0]):
            print("Unknown instruction!")

        elif("MOV" == str_split[0]):
            cpulib.CPUMov(self, str_split[1], str_split[2])

        elif("MVI" == str_split[0]):
            cpulib.CPUMvi(self, str_split[1], str_split[2])

        elif("LXI" == str_split[0]):
            cpulib.CPULxi(self, str_split[1], str_split[2])

        elif("LDA" == str_split[0]):
            cpulib.CPULda(self, str_split[1])

        elif("STA" == str_split[0]):
            cpulib.CPUSta(self, str_split[1])

        elif("LHLD" == str_split[0]):
            cpulib.CPULhld(self, str_split[1])

        elif("SHLD" == str_split[0]):
            cpulib.CPUShld(self, str_split[1])

        elif("LDAX" == str_split[0]):
            cpulib.CPULdax(self, str_split[1])

        elif("STAX" == str_split[0]):
            cpulib.CPUStax(self, str_split[1])
        
        elif("XCHG" == str_split[0]):
            cpulib.CPUXchg(self)
            
        elif("ADD" == str_split[0]):
            cpulib.CPUAdd(self, str_split[1])

        elif("ADI" == str_split[0]):
            cpulib.CPUAdi(self, str_split[1])
        
        elif("ADC" == str_split[0]):
            cpulib.CPUAdc(self, str_split[1])

        elif("ACI" == str_split[0]):
            cpulib.CPUAci(self, str_split[1])

        elif("SUB" == str_split[0]):
            cpulib.CPUSub(self, str_split[1])

        elif("SUI" == str_split[0]):
            cpulib.CPUSui(self, str_split[1])

        elif("SBB" == str_split[0]):
            cpulib.CPUSbb(self, str_split[1])

        elif("SBI" == str_split[0]):
            cpulib.CPUSbi(self, str_split[1])

        elif("INR" == str_split[0]):
            cpulib.CPUInr(self, str_split[1])

        elif("DCR" == str_split[0]):
            cpulib.CPUDcr(self, str_split[1])

        elif("INX" == str_split[0]):
            cpulib.CPUInx(self, str_split[1])

        elif("DCX" == str_split[0]):
            cpulib.CPUDcx(self, str_split[1])

        elif("DAD" == str_split[0]):
            cpulib.CPUDad(self, str_split[1])

        elif("DAA" == str_split[0]):
            print("Unimplemented instruction DAA at " + hex(im_pc) )

        elif("ANA" == str_split[0]):
            cpulib.CPUAna(self, str_split[1])

        elif("ANI" == str_split[0]):
            cpulib.CPUAni(self, str_split[1])

        elif("ORA" == str_split[0]):
            cpulib.CPUOra(self, str_split[1])

        elif("ORI" == str_split[0]):
            cpulib.CPUOri(self, str_split[1])

        elif("XRA" == str_split[0]):
            cpulib.CPUXra(self, str_split[1])

        elif("XRI" == str_split[0]):
            cpulib.CPUXri(self, str_split[1])

        elif("CMP" == str_split[0]):
            cpulib.CPUCmp(self, str_split[1])

        elif("CPI" == str_split[0]):
            cpulib.CPUCpi(self, str_split[1])

        elif("RLC" == str_split[0]):
            cpulib.CPURlc(self)

        elif("RRC" == str_split[0]):
            cpulib.CPURrc(self)

        elif("RAL" == str_split[0]):
            cpulib.CPURal(self)

        elif("RAR" == str_split[0]):
            cpulib.CPURar(self, str_split[1])

        elif("CMA" == str_split[0]):
            cpulib.CPUCma(self)

        elif("CMC" == str_split[0]):
            cpulib.CPUCmc(self)

        elif("STC" == str_split[0]):
            cpulib.CPUStc(self)

        elif("JMP" == str_split[0]):
            cpulib.CPUJmp(self, str_split[1])

        elif("CALL" == str_split[0]):
            cpulib.CPUCall(self, str_split[1])
            
        elif("RET" == str_split[0]):
            cpulib.CPURet(self)
            
        elif("RST" == str_split[0]):
            cpulib.CPURst(self, str_split[1])
            
        elif("PCHL" == str_split[0]):
            cpulib.CPUPchl(self)

        elif("POP" == str_split[0]):
            cpulib.CPUPop(self, str_split[1])

        elif("PUSH" == str_split[0]):
            cpulib.CPUPush(self, str_split[1])

        elif("XTHL" == str_split[0]):
            cpulib.CPUXthl(self)

        elif("SPHL" == str_split[0]):
            cpulib.CPUSphl(self)

        elif("IN" == str_split[0]):
            im_pc = self.getPairFull("PC")
            print("Unimplemented instruction IN " + hex(im_pc))

        elif("OUT" == str_split[0]):
            self.screen.ScreenDraw(self)

        elif("EI" == str_split[0]):
            print("Unimplemented instruction EI " + hex(im_pc))

        elif("DI" == str_split[0]):
            print("Unimplemented instruction DI " + hex(im_pc) )

        elif("HLT" == str_split[0]):
            print("CPU Halted!")

        elif("JZ" == str_split[0]):
            cpulib.CPUJcon(self, str_split[1], "Z")
            
        elif("JNZ" == str_split[0]):
            cpulib.CPUJncon(self, str_split[1], "Z")
            
        elif("JC" == str_split[0]):
            cpulib.CPUJcon(self, str_split[1], "C")           

        elif("JNC" == str_split[0]):
            cpulib.CPUJncon(self, str_split[1], "C")
            
        elif("JM" == str_split[0]):
            cpulib.CPUJcon(self, str_split[1], "S")
            
        elif("JP" == str_split[0]):
            cpulib.CPUJncon(self, str_split[1], "S")
            
        elif("JPE" == str_split[0]):
            cpulib.CPUJcon(self, str_split[1], "P")
            
        elif("JPO" == str_split[0]):
            cpulib.CPUJncon(self, str_split[1], "P")
                
        elif("CZ" == str_split[0]):
            cpulib.CPUCcon(self, str_split[1], "Z")
            
        elif("CNZ" == str_split[0]):
            cpulib.CPUCncon(self, str_split[1], "Z")
            
        elif("CC" == str_split[0]):
            cpulib.CPUCcon(self, str_split[1], "C")
            
        elif("CNC" == str_split[0]):
            cpulib.CPUCncon(self, str_split[1], "C")
            
        elif("CM" == str_split[0]):
            cpulib.CPUCcon(self, str_split[1], "S")
            
        elif("CP" == str_split[0]):
            cpulib.CPUCncon(self, str_split[1], "S")
            
        elif("CPE" == str_split[0]):
            cpulib.CPUCcon(self, str_split[1], "P")
            
        elif("CPO" == str_split[0]):
            cpulib.CPUCncon(self, str_split[1], "P")
            
        elif("RZ" == str_split[0]):
            cpulib.CPURcon(self, "Z")
            
        elif("RNZ" == str_split[0]):
            cpulib.CPURncon(self, "Z")
            
        elif("RC" == str_split[0]):
            cpulib.CPURcon(self, "C")
            
        elif("RNC" == str_split[0]):
            cpulib.CPURncon(self, "C")
            
        elif("RM" == str_split[0]):
            cpulib.CPURcon(self, "S")
            
        elif("RP" == str_split[0]):
            cpulib.CPURncon(self, "S")
        elif("RPE" == str_split[0]):
            cpulib.CPURcon(self, "P")
            
        elif("RPO" == str_split[0]):
            cpulib.CPURncon(self, "P")


    def CPUGetNextInstructionAddress(self):
        im_pc = self.getPairFull("PC") 
        str_instruction, opcode, im_pc = dislib.parseInstruction(self.list_memory, im_pc + 1)
        return im_pc

    def CPUExecute(self):
        im_pc = self.getPairFull("PC")
        str_instruction, opcode, im_nextPc = dislib.parseInstruction(self.list_memory, im_pc)

        self.advance = 1

        self.CPUJumpTable(str_instruction)

        if(self.advance == 1):
            im_pc = im_nextPc + 1
            self.setPairFull("PC", im_pc)


    def CPUBreak(self):
        im_pc = self.getPairFull("PC")
        reg_bp1 = self.getPairFull("BP1")
        reg_bp2 = self.getPairFull("BP2")
        reg_bp3 = self.getPairFull("BP3")
        bp = [reg_bp1, reg_bp2, reg_bp3]

        for i in bp:
            if(im_pc == i):
                return 1
        return 0



