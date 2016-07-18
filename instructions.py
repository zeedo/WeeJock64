import sys

from statusregister import StatusRegister


class Instructions(object):
    def nop(self):
        pass

    # BRANCH OPERATIONS

    def bcs(self):
        if self.P.carry:
            self.PC = self.address_pointer

    def bcc(self):
        if not self.P.carry:
            self.PC = self.address_pointer

    def beq(self):
        if self.P.zero:
            self.PC = self.address_pointer

    def bne(self):
        if not self.P.zero:
            self.PC = self.address_pointer

    def bpl(self):
        if not self.P.negative:
            self.PC = self.address_pointer

    def bmi(self):
        if self.P.negative:
            self.PC = self.address_pointer

    def bvc(self):
        if not self.P.overflow:
            self.PC = self.address_pointer

    def bvs(self):
        if self.P.overflow:
            self.PC = self.address_pointer

    def rts(self):
        low_byte = self.pop()
        high_byte = self.pop()
        self.set_PC_bytes(high_byte, low_byte)
        self.PC += 1

    def jsr(self):
        # Prep for the RTS instruction which pulls us back to the current PC
        self.PC -= 1
        high_byte, low_byte = self.get_PC_bytes()
        self.push(high_byte)
        self.push(low_byte)

        # Jump to the required subroutine
        self.PC = self.address_pointer

        if self.PC == 0xFFD2:  # Fake the CHROUT Routine http://sta.c64.org/cbm64krnfunc.html
            sys.stdout.write(chr(self.A)),
            self.rts()  # Execute the return, pop's the PC back off the stack

    def jmp(self):
        self.PC = self.address_pointer
        # print(hex(self.address_pointer))

    # FLAG OPERATIONS

    def clc(self):
        self.P.carry = 0

    def sec(self):
        self.P.carry = 1

    def cli(self):
        self.P.interrupt = 0

    def sei(self):
        self.P.interrupt = 1

    def clv(self):
        self.P.overflow = 0

    def cld(self):
        self.P.decimal = 0

    def sed(self):
        self.P.decimal = 1

    # BIT OPERATIONS
    def _and(self):  # Reserved keyword therefore underscored
        self.A = self.A & self.ram[self.address_pointer]
        self.P.zero = (self.A == 0)
        self.P.negative = ((self.A & 0b10000000) >> 7)

    def bit(self):
        self.P.zero = (self.ram[self.address_pointer] & self.A == 0)
        self.P.negative = ((self.ram[self.address_pointer] & 0b10000000) >> 7)
        self.P.overflow = ((self.ram[self.address_pointer] & 0b01000000) >> 6)

    def ora(self):
        self.A = self.A | self.ram[self.address_pointer]
        self.P.zero = (self.A == 0)
        self.P.negative = ((self.A & 0b10000000) >> 7)

    def eor(self):
        self.A = self.A ^ self.ram[self.address_pointer]
        self.P.zero = (self.A == 0)
        self.P.negative = ((self.A & 0b10000000) >> 7)

    # MEMORY OPERATiONS

    def lda(self):
        self.A = self.ld_reg()

    def ldx(self):
        self.X = self.ld_reg()

    def ld_reg(self):
        reg = self.ram[self.address_pointer]
        self.P.zero = (reg == 0)
        self.P.negative = ((reg & 0b10000000) >> 7)
        return reg

    def sta(self):
        self.ram[self.address_pointer] = self.A

    def stx(self):
        self.ram[self.address_pointer] = self.X

    # OTHER OPERATIONS

    def brk(self):
        # TODO: Implement proper BRK handler
        print("\n[!] BREAK at " + hex(self.PC))
        exit(0)

    # STACK INSTRUCTIONS


    def txs(self):
        self.SP = self.X

    def tsx(self):
        self.X = self.SP

    def pha(self):
        self.push(self.A)

    def pla(self):
        self.A = self.pop()
        self.P.zero = (self.A == 0)
        self.P.negative = ((self.A & 0b10000000) >> 7)

    def php(self):
        # PHP Sets bits 4 and 5 to 1
        # http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior
        self.push(self.P.flags | 0b000110000)

    def plp(self):
        pulled_reg = StatusRegister()
        pulled_reg.flags = self.pop()
        self.P.negative = pulled_reg.negative
        self.P.overflow = pulled_reg.overflow
        # Ignores BRK bit and unused bit
        # http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior
        self.P.decimal = pulled_reg.decimal
        self.P.interrupt = pulled_reg.interrupt
        self.P.zero = pulled_reg.zero
        self.P.carry = pulled_reg.carry

    # COMPARISON INSTRUCTIONS

    def cmp(self):
        if self.A >= self.ram[self.address_pointer]:
            self.P.negative = 0
            self.P.carry = 1
            if self.A == self.ram[self.address_pointer]:
                self.P.zero = 1
        elif self.A < self.ram[self.address_pointer]:
            self.P.negative = 1
            self.P.carry = 0
            self.P.zero = 0
