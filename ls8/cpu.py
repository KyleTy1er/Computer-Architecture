"""CPU functionality."""

import sys

PRN = 0b01000111
HLT = 0b00000001
LDI = 0b10000010


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.ir = 0
        self.mar = []
        self.mdr = []

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
                if line.startswith('#') or line.startswith('\n'):
                    continue
                else:
                    instruction = line.split(' ')[0]
                    self.ram[address] = int(instruction, 2)
                    address += 1

    # def load(self, file):
    #     """Load a program into memory."""
    #     # file = sys.argv[1]
    #
    #
    #     address = 0
    #     with open(file) as f:
    #         for line in f:
    #             line = line.split("#")
    #             try:
    #                 v = int(line[0])
    #                 self.ram[address] = v
    #                 address += 1
    #             except ValueError:
    #                 continue

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
            ir = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                running = False
            else:
                self.dispatchtable[ir](reg_a, reg_b)
