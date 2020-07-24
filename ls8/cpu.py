
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
MUL = 0b10100010
ADD = 0b10100000
CMP = 0b10100111

# Main CPU class
class CPU:
    # Construct a new CPU
    def __init__(self):
        #The LS-8 has 8-bit addressing, so can address 256 bytes of RAM total.
        self.ram = [0] * 256
        # 8 general-purpose 8-bit numeric registers R0-R7.
        self.register = [0] * 8
        # Program Counter, address of the currently executing instruction
        self.pc = 0
        # The SP points at the value at the top of the stack (most recently pushed), or at
        # address F4 if the stack is empty.
        self.sp = 7
        # The flags register FL holds the current flags status.
        # These flags can change based on the operands given to the CMP opcode.
        self.fl = 0

        self.dispatchtable = {
            MUL: self.mul,
            ADD: self.add,
            CMP: self.cmp,
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }

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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, op_a, op_b):
        if op == "ADD":
            self.register[op_a] += self.register[op_b]
        elif op == "MUL":
            self.register[op_a] *= self.register[op_b]
        elif op == "CMP":
            self.fl = 1 if self.register[op_a] == self.register[op_b] else 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def mul(self, op_a, op_b):
        '''
        Multiply the values in two registers together and store the result in registerA.
        '''
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    def add(self, op_a, op_b):
        '''
        Add the value in two registers and store the result in registerA.
        '''
        self.alu("ADD", op_a, op_b)
        self.pc += 3


    def cmp(self, op_a, op_b):
        '''
        Compare the values in two registers.

        If they are equal, set the Equal E flag to 1, otherwise set it to 0.

        If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.

        If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
        '''

        self.alu("CMP", op_a, op_b)
        self.pc += 3

    def prn(self, op_a, op_b):
        '''
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        '''
        print(self.register[op_a])
        self.pc += 2

    def ldi(self, op_a, op_b):
        '''
        If E flag is clear (false, 0), jump to the address stored in the given register.
        '''
        self.register[op_a] = op_b
        self.pc += 3

    def push(self, op_a, op_b):
        '''
        Push the value in the given register on the stack.
        Decrement the SP.
        Copy the value in the given register to the address pointed to by SP.
        '''
        self.sp -= 1
        self.ram_write(self.sp, self.register[op_a])
        self.pc += 2

    def pop(self, op_a, op_b):
        '''
        Pop the value at the top of the stack into the given register.

        Copy the value from the address pointed to by SP to the given register.
        Increment SP.
        '''
        self.register[op_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def call(self, op_a, op_b):
        '''
        Calls a subroutine (function) at the address stored in the register.
        The address of the instruction directly after CALL is pushed onto the stack. This allows us to return to where
        we left off when the subroutine finishes executing.
        The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first
        instruction in the subroutine. The PC can move forward or backwards from its current location.
        '''
        self.sp -= 1
        self.ram_write(self.sp, self.pc + 2)
        self.pc = self.register[op_a]

    def ret(self, op_a, op_b):
        '''
        Return from subroutine.
        Pop the value from the top of the stack and store it in the PC.
        '''
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def jmp(self, op_a, op_b):
        '''
        Jump to the address stored in the given register.
        Set the PC to the address stored in the given register.
        '''
        self.pc = self.register[op_a]

    def jeq(self, op_a, op_b):
        '''
        If equal flag is set (true), jump to the address stored in the given register.

        '''
        if self.fl:
            self.jmp(op_a, op_b)
        else:
            self.pc += 2

    def jne(self, op_a, op_b):
        '''
        If E flag is clear (false, 0), jump to the address stored in the given register.
        '''
        if not self.fl:
            self.jmp(op_a, op_b)
        else:
            self.pc += 2

    def run(self):
        running = True

        while running:
            # Instruction Register, contains a copy of the
            # currently executing instruction:
            ir = self.ram_read(self.pc)
            # op_a and op_b contain the two operands
            # of each set of instructions
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                '''
                Halt the CPU (and exit the emulator).
                '''
                running = False
            else:
                self.dispatchtable[ir](op_a, op_b)