

# Day 2 Notes

'''



Bitwise Operations

Truth Table

Boolean:

A  B            A and B
-----------------------
F  F              F
F  T              F
T  F              F
T  T              T

if a > 10 and a < 20:
    do something


Bitwise:

A  B            A and B
-----------------------
0  0              0
0  1              0
1  0              0
1  1              1



324 & 67 = 64     why?

do bitwise on the columns and you get the bitwise result:

0b11101010
0b00111100   "AND mask"
----------
0b00101000

what is the point of doing this ... what does doing the "&" of two numbers
accomplish for us?

if the first two bits denote 2.. the total length of the instruction must be 3
so we must move the PC 3 times to cover the instruction:

Instruction Layout

Meanings of the bits in the first byte of each instruction: AABCDDDD

AA Number of operands for this opcode, 0-2
B 1 if this is an ALU operation
C 1 if this instruction sets the PC
DDDD Instruction identifier



To extract bits

LDI

1) Mask

  0b10000010
& 0b11000000
------------
  0b10000000

2) Shift

need to shift right 6 times:   aka divide by base 6 times:
   123456
0b10000000
     =
0b00000010



example:

trying to get the number 34

1) mask

123456
009900
------
003400

2) shift

03400 right shift twice
00034


number of operands = instruction value
instruction length = number of operands + 1


we can get rid of bits with AND
we can set bits with OR


Clearing bits-------------------- AND

everywhere you AND will be cleared

0b11100011
0b11011111
----------
0b11000011


Setting bits---------------------- OR

0b11100011
0b00001000
----------
0b11101011



'''

# Day 2 Assignment Notes
'''
ALU is for performing arithmetic -

So ALU should handle multiply

.ls8 file type has no meaning - they are technically ASCII text files

'''