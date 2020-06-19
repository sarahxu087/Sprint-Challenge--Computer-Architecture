"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
POP = 0b01000110
PUSH = 0b01000101
SP = 7
CALL = 0b01010000
RET = 0b00010001
CMP= 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
ltf = 0b100
gtf = 0b010
etf = 0b001
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.pc = 0
        self.reg= [0]*8
        self.reg[SP] = 0xf4
        self.fl=0

    def load(self,filename):
        """Load a program into memory."""
        '''
        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        '''
        try:
            address = 0
            # sys.argv[0] is the name of the running program itself
            filename = sys.argv[1]
            with open(filename) as f:
                for line in f:
                    # ignore comments
                    comment_split = line.split('#')
                    # strip out whitespace
                    num = comment_split[0].strip()
                    # ignore blank lines
                    if num == "":
                        continue
                    # convert the binary string to integers.
                    # built-in integer function dose it for us.
                    value = int(num,2)

                    self.ram[address] = value
                    address+=1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)


        
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] *=self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a]<self.reg[reg_b]:
                self.fl = ltf
            elif self.reg[reg_a]>self.reg[reg_b]:
                self.fl = gtf
            else:
                self.fl = etf

        
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""


        running = True
        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == LDI:
                self.reg[operand_a]=operand_b
                self.pc +=3
            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc +=2
            elif ir == MUL:
                self.alu(ir,operand_a,operand_b)
                self.pc +=3
            elif ir == ADD:
                self.alu(ir,operand_a,operand_b)
                self.pc +=3
            elif ir == CMP:
                self.alu(ir,operand_a,operand_b)
                self.pc +=3
            elif ir == PUSH:
                self.reg[SP]-=1
                value = self.reg[operand_a]
                self.ram[self.reg[SP]]=value
                self.pc +=2
            elif ir == POP:
                value = self.ram[self.reg[SP]]
                self.reg[operand_a] = value
                self.reg[SP]+=1
                self.pc +=2
            elif ir == CALL:
                return_addr = self.pc+2
                self.reg[SP]-=1
                self.ram[self.reg[SP]]=return_addr
                self.pc = self.reg[operand_a]
            elif ir == JMP:
                self.pc = self.reg[operand_a]
            elif ir == JEQ:
                if self.fl & etf:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc +=2
            elif ir == JNE:
                if not self.fl & etf:
                    self.pc =self.reg[operand_a]
                else:
                    self.pc+=2
                

                
            elif ir == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] +=1
            

            elif ir == HLT:
                running = False
            else:
                print(f'Unknown instruction{ir} at address{self.pc}')
                sys.exit(1)

    
    def ram_read(self,address):
        return self.ram[address]
    def ram_write(self,value,address):
        self.ram[address]=value
        
