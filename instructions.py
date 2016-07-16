import sys

import numpy as np


class Instructions(object):
    def nop(self):
        pass

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


    def brk(self):
        # TODO: Implement proper BRK handler
        print("\n[!] BREAK at " + hex(self.PC))
        exit(0)

    def clc(self):
        self.P.carry = 0

    def lda(self):
        self.A = self.ld_reg()

    def ldx(self):
        self.X = self.ld_reg()

    def ld_reg(self):
        reg = self.ram[self.address_pointer]
        self.P.zero = (reg == 0)
        self.P.negative = ((reg & 0b10000000) >> 7)
        return reg

    def bit(self):
        self.P.zero = (self.ram[self.address_pointer] & self.A == 0)
        self.P.negative = ((self.ram[self.address_pointer] & 0b10000000) >> 7)
        self.P.overflow = ((self.ram[self.address_pointer] & 0b01000000) >> 6)


    def sec(self):
        self.P.carry = 1

    def sta(self):
        self.ram[self.address_pointer] = self.A

    def stx(self):
        self.ram[self.address_pointer] = self.X

    def jsr(self):
        # TODO: replace PC_fake_retaddr with a stack push
        self.PC_fake_retaddr = np.copy(self.PC)
        self.PC = self.address_pointer

        if self.PC == 0xFFD2:  # Fake the CHROUT Routine http://sta.c64.org/cbm64krnfunc.html
            sys.stdout.write(chr(self.A)),
            self.PC = self.PC_fake_retaddr
            self.address_pointer = None


    def jmp(self):
        self.PC = self.address_pointer
        # print(hex(self.address_pointer))
