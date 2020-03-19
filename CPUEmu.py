import core as corelib
import copy
import time

class CPUState(object):
	def __init__(self):

		self.core = corelib.Core()
		self.lastState = []
		self.currIteration = -1 
		
	def CPUEmulateInstruction(self):

		self.core.setPairFull("BP1", 6714)
		self.core.setPairFull("BP2", -1)
		self.core.setPairFull("BP3", -1)


		while(True):

			str_shell = input()

			if(str_shell == ""):
				self.core.CPUExecute()
				self.lastState.append(copy.deepcopy(self.core))
				self.currIteration = self.currIteration + 1

			elif(str_shell[0] == "B"):
				str_shell = str_shell.split(" ")
				self.core.setPairFull("BP2", int(str_shell[1], 16))

			elif(str_shell[0] == "P"):
				if(len(str_shell) == 1):
					self.core = self.lastState[self.currIteration - 1]
				else:
					str_shell = str_shell.split(" ")
					self.core = self.lastState[self.currIteration - int(str_shell[1])]

				self.core.printCPUState()

			elif(str_shell == "R"):
				try:
					while(self.core.CPUBreak() != 1):
						self.core.CPUExecute()
						self.currIteration = self.currIteration + 1
						#print( str(self.core.getPairFull("BP1")) + " : " + hex(self.core.getPairFull("PC")) )
				except KeyboardInterrupt:
					pass

			self.core.printCPUState()
import core as corelib
import copy
import time

class CPUState(object):
	def __init__(self):

		self.core = corelib.Core()
		self.lastState = []
		self.currIteration = -1 
		
	def CPUEmulateInstruction(self):

		self.core.setPairFull("BP1", 0xada)
		self.core.setPairFull("BP2", -1)
		self.core.setPairFull("BP3", -1)
		self.core.printCPUState()

		while(True):

			str_shell = input()

			if(str_shell == ""):
				self.core.CPUExecute()
				#self.lastState.append(copy.deepcopy(self.core))
				#self.currIteration = self.currIteration + 1
				self.core.printCPUState()

			elif(str_shell[0] == "B"):
				str_shell = str_shell.split(" ")
				self.core.setPairFull("BP2", int(str_shell[1], 16))

			elif(str_shell[0] == "P"):
				if(len(str_shell) == 1):
					self.core = self.lastState[self.currIteration - 1]
				else:
					str_shell = str_shell.split(" ")
					self.core = self.lastState[self.currIteration - int(str_shell[1])]

				self.core.printCPUState()

			elif(str_shell == "R"):
				try:
					while(self.core.CPUBreak() != 1):
						self.core.CPUExecute()
				except KeyboardInterrupt:
					pass

			self.core.printCPUState()

def main():
	c = CPUState()
	c.CPUEmulateInstruction()


if __name__ == "__main__":
	main()





def main():
	c = CPUState()
	c.CPUEmulateInstruction()


if __name__ == "__main__":
	main()




