

# Notes Day 1

'''

 NUMBER BASES
 ------------

 Base 2 (Binary)
 Base 8 (Octal)
 Base 10 (Decimal)
 Base 16 (Hexadecimal)
 Base 64 ()

Base is how many digits you have at your disposal.
The number of digits determines when you need to start
stacking your numbers positionally.


Base 64 comprised of
uppercase letters: 26
lowercase letters: 26
numbers: 10
symbols "+", "/": 2


COUNTING
--------

Base 10
one's place - represents how many ones we have
0 - 0 ones
1 - 1 ones
2 -  2 ones
3 - 3 ones
4
5
6
7
8
9

now we add a second column:

ten's place - represents how many tens we have
10 <---- 1 ten and 0 zeroes
11 - 1 ten and 1 ones
12 - 1 ten and 2 ones


Base 2
32 16  8  4  2  0
00|00|00|00|00|00

As we raise to a power that indicates the value of a column


2^0 == 1
2^1 == 2
2^2 == 4
2^3 == 8

saying binary 10 is the same as decimal 2 is accurate.

00 - zero == decimal 0
01 - one == decimal 1
10 - two == decimal 2
11 - three == decimal 3
100 - four == decimal 4
101 - five
110 - six
111 - seven
1000 - eight

When we see a number how do we know or indicate 
the number is one base or another??

step 1. equate the digits
step 2. convert according to digits
step 3. combine results

a = 12 - default is 10
a = 0b1100 - this tells python we want binary

4 binary digits ==== 1 hex digit

binary digit contracted is ... bit.

0x indicate hexadecimal:

0x 2A is 42 in hexadecimal... convert to binary?

in hex 2 = 2
in hex A = 10

in binary 2 = 0010
in binary 10 = 1010

add these up

101010

0x  2   |  A
   vvvv |wwwww

19 in hexadecimal?
one 16, and 3 ones:
13


8 bits = "byte"
4 bits = "nibble" ... 4fun. or "nybble"

kilo == 1024   == 2^10
mega = 1048576 == 2^20



'''

# Assignment Notes:

'''
CPU
    executing instructions
    gets them out of RAM
    registers (like variables)
        Fixed Names - R0-R7
        Fixed Number - 8
        Fixed Size - 8 bits
    
    
Memory (RAM)
    A big array of bytes
    Each memory slot has an index, and a value stored at that index
    that index into memory AKA;
        pointer 
        lcoation
        address
        
0b00000000 == decimal 0
0b11111111 == decimal 255

**** POINTERS ****

there is a high level readme, but there is an LS8 readme that has more detailed steps
should be able to figure out which steps correspond to your day's tasks
ignore the ASM directory for now - 
FAQ is helpful to skim -
LS-8 is where all the info is , but it is not a guide... it is specs.
You can ignore flags, interrupts for now. You just need to implement MVP for the day.
HLT is like break
LDI is like save register
and PRN is like print register
 LOOK FOR LSM print hello world

'''

# this is the core of what your emulator will be like "conceptually".
# instructions can take variable number of bytes to represent
# how does the CPU know the difference between 2 and 2 for diff instructions?
# when you run a 3 you should increment the number of bytes for that instruction
# make sure you land on valid instructions by incrementing the PC by the correct amount

memory = [

    1,  # print this
    1,  # print this  # halt
    3,  # Save Register... save R2, 99 (r2 in register should have value 99)
    2,  # R2
    99, # 99
    4,  # print reg R2
    2,  # R2
    2,# halt
]

register = [0] * 8

# this creates [0, 0, 0, 0, 0, 0, 0, 0]

pc = 0  # program counter, index into memory of the current instruction
        # AKA a pointer to the current instruction

# switch on
running = True

while running:
    i = memory[pc]
    if i == 1:
        print("this")
        # must move to next instruction
        pc += 1
    elif i == 2:
        # switch off
        running = False
    elif i == 3: # save reg
        reg_num = memory[pc +1]
        value = memory[pc +2]
        register[reg_num] = value
        pc += 3
    elif i == 4:
        reg_num = memory[pc + 1]
        print (register[reg_num])
        pc += 2
    else:
        print("unknown instruction {i}")


print(register)
