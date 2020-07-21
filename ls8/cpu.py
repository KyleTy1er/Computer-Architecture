"""CPU functionality."""

import sys

PRN = 0b01000111
HLT = 0b00000001
LDI = 0b10000010


class CPU:
    """Main CPU class."""

    def __init__(self):
        # The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256
        # These registers only hold values between 0-255.
        self.register = [0] * 8
        # PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        # IR: Instruction Register, contains a copy of the currently executing instruction
        self.ir = 0
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        self.mar = 0
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.mdr = 0

        self.dispatchtable = {
            PRN: self.prn,
            LDI: self.ldi,
        }

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

    def prn(self, reg_a, reg_b):
        print(self.register[reg_a])
        self.pc += 2

    def ldi(self, reg_a, reg_b):
        self.register[reg_a] = reg_b
        self.pc += 3

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
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
            self.trace()
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
            else:
                self.dispatchtable[ir](reg_a, reg_b)
