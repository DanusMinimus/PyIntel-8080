#[---8 Bit load/store operations group]

#Advanced nth times in cpu

#[---8 Bit load/store operations group]
def CPUMov(core, reg_a, reg_b):
	im_b = core.getReg(reg_b)
	core.setReg(reg_a, im_b)

def CPUMvi(core, reg_a, im_b):
	core.setReg(reg_a, im_b)

def CPUStax(core, reg_a):
	memory_a, memory_b = core.getPair(reg_a)
	memory = core.setImPair(memory_a, memory_b)
	core.setMemory(memory, core.getReg("A"))

def CPULdax(core, reg_a):
	memory_a, memory_b = core.getPair(reg_a)
	memory = core.setImPair(memory_a, memory_b)
	core.setReg("A", core.getMemory(memory))

def CPUSta(core, im_a):
	core.setMemory(im_a, core.getReg("A"))

def CPULda(core, im_a):
	core.setReg("A", core.getMemory(im_a))
#[---8 Bit load/store operations group]

#[---16 Bit load/store operations group]
def CPULxi(core, reg_a, im_all):
	im_high, im_low = core.getImPair(im_all)
	core.setPair(reg_a, im_high, im_low)

def CPUShld(core, im_b):
	high, low = core.getPair("H")
	core.setMemory(im_b + 1, high)
	core.setMemory(im_b, low)

def CPULhld(core, im_b):
	high_memory = core.getMemory(im_b + 1)
	low_memory = core.getMemory(im_b)
	core.setPair("H", high_memory, low_memory)

def CPUPush(core, reg_a):
	reg_sp = core.getPairFull("SP")
	im_high, im_low = core.getPair(reg_a)

	core.setMemory(reg_sp - 1, im_high)
	core.setMemory(reg_sp - 2, im_low)

	reg_sp = reg_sp - 2

	core.setPairFull("SP", reg_sp)

def CPUPop(core, reg_a):
	reg_sp = core.getPairFull("SP")

	im_high = core.getMemory(reg_sp + 1)
	im_low = core.getMemory(reg_sp)

	im_new = core.setImPair(im_high, im_low)

	core.setPairFull(reg_a, im_new)

	reg_sp = reg_sp + 2

	core.setPairFull("SP", reg_sp)



def CPUXthl(core):

	reg_sp = core.getPairFull("SP")

	reg_h, reg_l = core.getPair("H")

	im_high = core.getMemory(reg_sp + 1)
	im_low = core.getMemory(reg_sp)

	core.setPair("H", im_high, im_low)

	core.setMemory(reg_sp + 1, reg_h)
	core.setMemory(reg_sp, reg_l)


def CPUSphl(core):
	h, l = core.getPair("H")
	im_hl = core.setImPair(h, l)
	core.setPairFull("SP", im_hl)

def CPUXchg(core):
	h, l = core.getPair("H")
	d, e = core.getPair("D")
	core.setPair("D", h, l)
	core.setPair("H", d, e)
	
#[---16 Bit load/store operations group]

#[---8 Bit arithmatics operations group]

def CPUAdd(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc + im_a)
	core.setFlags(im_acc + im_a)

def CPUSub(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc - im_a)
	core.setFlags(im_acc - im_a)

def CPUAna(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc & im_a)
	core.setFlags(im_acc & im_a)

def CPUOra(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc | im_a)
	core.setFlags(im_acc | im_a)

def CPUAdc(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc + im_a + core.condition_bits["C"])
	core.setFlags(im_acc + im_a + core.condition_bits["C"])

def CPUSbb(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc - im_a - core.condition_bits["C"])
	core.setFlags(im_acc - im_a - core.condition_bits["C"])

def CPUXra(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc ^ im_a)
	core.setFlags(im_acc ^ im_a)

def CPUOra(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	core.setReg("A", im_acc | im_a)
	core.setFlags(im_acc | im_a)

def CPUCmp(core, reg_a):
	im_a = core.getReg(reg_a)
	im_acc = core.getReg("A")
	im_cmp = im_acc - im_a
	core.setFlags(im_cmp)

def CPUAdi(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc + im_a)
	core.setFlags(im_acc + im_a)

def CPUSui(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc - im_a)
	core.setFlags(im_acc - im_a)

def CPUAni(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc & im_a)
	core.setFlags(im_acc & im_a)

def CPUOri(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc | im_a)
	core.setFlags(im_acc | im_a)

def CPUAci(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc + (im_a + core.condition_bits["C"]))
	core.setFlags(im_acc + (im_a + core.condition_bits["C"]))


def CPUSbi(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc - im_a - core.condition_bits["C"])
	core.setFlags(im_acc - im_a - core.condition_bits["C"])

def CPUXri(core, im_a):
	im_acc = core.getReg("A")
	core.setReg("A", im_acc  ^ im_a)
	core.setFlags(im_acc ^ im_a)

def CPUCpi(core, im_a):
	im_acc = core.getReg("A")
	im_cmp = im_acc - im_a
	core.setFlags(im_cmp)

def CPUInr(core, reg_a):
	im_reg = core.getReg(reg_a)
	core.setReg(reg_a, im_reg + 1)
	core.setFlags(im_reg + 1, "TC")

def CPUDcr(core, reg_a):
	im_reg = core.getReg(reg_a)
	core.setReg(reg_a, im_reg - 1)
	core.setFlags(im_reg - 1, "TC")

def CPUCmc(core):
	core.condition_bits["C"] = (~core.condition_bits["C"]) & 1
	core.setReg("FLAGS", core.getNewFlagReg())

def CPUStc(core):
	core.condition_bits["C"] = 1
	core.setReg("FLAGS", core.getNewFlagReg())

def CPUCma(core):
	im_acc = core.getReg("A")
	core.setReg("A", (~im_acc))

def CPURlc(core):
	im_acc = core.getReg("A")
	im_acc = (im_acc << 1) | core.condition_bits["C"]

	im_acc_prev = core.getReg("A")
	core.condition_bits["C"] = int(format(im_acc_prev, "b").zfill(8)[0])

	core.setReg("A", im_acc)
	core.setReg("FLAGS", core.getNewFlagReg())

def CPURrc(core):
	im_acc = core.getReg("A")
	im_acc = (im_acc >> 1) | (core.condition_bits["C"] * 0xff)

	im_acc_prev = core.getReg("A")
	core.condition_bits["C"] = int(format(im_acc_prev, "b").zfill(8)[7])

	core.setReg("A", im_acc)
	core.setReg("FLAGS", core.getNewFlagReg())

def CPURal(core):
	im_acc = core.getReg("A")
	im_acc = (im_acc << 1) | (core.condition_bits["C"])

	core.condition_bits["C"] = int(format(core.getReg("A"), "b").zfill(8)[0])
	core.setReg("A", im_acc)

	core.setReg("FLAGS", core.getNewFlagReg())

def CPURar(core):
	im_acc = core.getReg("A")
	im_acc = (im_acc >> 1) | (core.condition_bits["C"]*128)

	core.condition_bits["C"] = int(format(core.getReg("A"), "b").zfill(8)[7])
	core.setReg("A", im_acc)

	core.setReg("FLAGS", core.getNewFlagReg())


#[---8 Bit arithmatics operations group]

#[---16 Bit arithmatics operations group]

def CPUDad(core, reg_a):
	high, low = core.getPair(reg_a)
	h_reg, l_reg = core.getPair("H")

	l_reg = (l_reg + low)

	core.setFlags(l_reg, "FC")

	h_reg = (h_reg + high + core.condition_bits["C"])

	core.setFlags(h_reg, "FC")

	core.setPair("H", h_reg, l_reg )

def CPUInx(core, reg_a):

	high, low = core.getPair(reg_a)

	low = (low + 1) & 0x1ff

	high = (high + (low >> 8) )

	core.setPair(reg_a, high, low )

def CPUDcx(core, reg_a):

	high, low = core.getPair(reg_a)

	low = (low - 1) & 0x1ff

	high = (high - (low >> 8) )

	core.setPair(reg_a, high, low)

#[---16 Bit arithmatics group]

#[---16 Bit branch operations group]

def CPUPchl(core):
	im_hl = core.getPairFull("H")
	core.setPairFull("PC", im_hl)

def CPUJmp(core, im_a):
	core.advance = 0
	core.setPairFull("PC", im_a)

def CPUJcon(core, im_a, c_bit):
	if(1 == core.condition_bits[c_bit]):
		CPUJmp(core, im_a)

def CPUJncon(core, im_a, c_bit):
	if(0 == core.condition_bits[c_bit]):
		CPUJmp(core, im_a)

def CPUCall(core, im_a):
	core.advance = 0
	CPUPush(core, "PC")
	CPUJmp(core, im_a)

def CPUCcon(core, im_a, c_bit):
	if(1 == core.condition_bits[c_bit]):
		CPUCall(core, im_a)

def CPUCncon(core, im_a, c_bit):
	if(0 == core.condition_bits[c_bit]):
		CPUCall(core, im_a)

def CPURet(core):
	CPUPop(core, "PC")

	reg_pc = core.getPairFull("PC")
	CPUJmp(core, reg_pc + 3)

def CPURcon(core, c_bit):
	if(1 == core.condition_bits[c_bit]):
		CPURet(core)

def CPURncon(core, c_bit):
	if(0 == core.condition_bits[c_bit]):
		CPURet(core)

def CPURst(core, im_a):
	CPUPush(core, "PC")
	CPUJmp(im_a << 3)


#[---16 Bit branch operations group]