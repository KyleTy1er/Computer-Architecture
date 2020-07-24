"""CPU functionality."""

import sys

PRN = 0b01000111
HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

# in a way these "instructions" are merely triggers by which we set up conditionals to fire off
# functions at certain index locations in self.ram and self.register


class CPU:
    """Main CPU class."""

# R7 is Stack Pointer (SP)
# [0, 0, 0, 0, 0, 0,  SP, 0]

    def __init__(self):
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256
        # These registers only hold values between 0-255.
        self.register = [0] * 8
        self.sp = 7
        # PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        # IR: Instruction Register, contains a copy of the currently executing instruction
        self.ir = 0
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.fl = 0
    def ram_read(self, mar):
        '''
        should accept the address to read and return the value stored there.
        '''

        return self.ram[mar]


    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self, file_name):
        address = 0

        with open(file_name, 'r') as f:
            for line in f:
                # ignore comments and new lines
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    instruction = line.split(' ')[0]
                    # specify base 2 as you read in lines to memory
                    self.ram[address] = int(instruction, 2)
                    address += 1

    # def pc_calc(self):

    def cmp(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    def jne(self, reg_a, reg_b):
        if not self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2

    def jmp(self, reg_a, reg_b):
        self.pc = self.register[reg_a]

    def jeq(self, reg_a, reg_b):
        if self.fl:
            self.jmp(reg_a, reg_b)

        if not self.fl:
            self.jmp(reg_a, reg_b)
        else:
            self.pc += 2

    def prn(self, reg_a, reg_b):
        '''
        PRN register pseudo-instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        '''

        print(self.register[reg_a])
        self.pc += 2

    def ldi(self, reg_a, reg_b):
        '''
        LDI register immediate
        Set the value of a register to an integer.
        '''

        self.register[reg_a] = reg_b
        self.pc += 3

    def push(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.register[reg_a])
        self.pc += 2

    def pop(self, reg_a, reg_b):
        self.register[reg_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def call(self, reg_a, reg_b):
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.register[reg_a]

    def ret(self, reg_a, reg_b):
        self.pc = self.ram_read(self.sp)
        self.sp += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "CMP":
            self.fl = 1 if self.register[reg_a] == self.register[reg_b] else 0
            self.pc +=3

        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()



    def run(self):

        running = True

        while running:
            # self.trace()
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if ir == HLT:
                running = False
            elif ir == PRN:
                self.prn(reg_a, reg_b)
            elif ir == ADD:
                op =  "ADD"
                self.alu(op, reg_a, reg_b)
            elif ir == LDI:
                self.ldi(reg_a, reg_b)
            elif ir == MUL:
                self.mul(reg_a, reg_b)
            elif ir == PUSH:
                self.push(reg_a, reg_b)
            elif ir == POP:
                self.pop(reg_a, reg_b)
            elif ir == CALL:
                self.call(reg_a, reg_b)
            elif ir == RET:
                self.ret(reg_a, reg_b)
            elif ir == JMP:
                self.jmp(reg_a, reg_b)
            elif ir == JNE:
                self.jne(reg_a, reg_b)
            elif ir == JEQ:
                self.jeq(reg_a, reg_b)
            elif ir == CMP:
                op =  "CMP"
                self.alu(op, reg_a, reg_b)

            else:
                print("something ain't right")


