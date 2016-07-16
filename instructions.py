import numpy as np
import sys


class Instructions(object):

    def nop(self):
        pass

    def brk(self):
        # TODO: Implement proper BRK handler
        print("\n[!] BREAK at " + hex(self.PC))
        exit(0)

    def lda(self):
        self.A = self.ram[self.address_pointer]

    def ldx(self):
        self.X = self.ram[self.address_pointer]

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
