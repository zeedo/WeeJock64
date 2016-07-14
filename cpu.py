import datetime
import timeit

import hexdump
import numpy as np
import struct
import sys
import opcode_table

MOS_65XX_RAM_START = 0xC000
MOS_65XX_RAM_SIZE = 0xFFFF


class StatusRegister(object):
    """MOS P Register, individual flags as booleans"""

    def __init__(self):
        # http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior

        self.carry = 0  # Carry: 1 if last addition or shift resulted in a carry,
        # or if last subtraction resulted in no borrow
        self.zero = 0  # Zero: 1 if last operation resulted in a 0 value
        self.interrupt = 1  # Interrupt: Interrupt inhibit - interrupts are disabled if this is true!
        self.decimal = 0  # Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
        self.breakflag = 0  # Clear if interrupt vectoring, set if BRK or PHP
        self.unused = 1  # Always set
        self.overflow = 0  # Overflow: 1 if last ADC or SBC resulted in signed overflow
        self.negative = 0  # Negative: Set to bit 7 of the last operation

    @property
    def flags(self):
        """Packs all the status flags into a uint8 """
        return np.packbits([self.carry,
                            self.zero,
                            self.interrupt,
                            self.decimal,
                            self.breakflag,
                            self.unused,
                            self.overflow,
                            self.negative])[0]  # packbits returns an array but we only want the single element

    @flags.setter
    def flags(self, P):
        """Unpacks status flags from an int """
        self.carry, self.zero, self.interrupt, self.decimal, self.breakflag, self.unused, self.overflow, self.negative = np.unpackbits(
            np.asarray(P, dtype="uint8"))

    def __str__(self):
        return "Flags:\tCZIDuuON\n\t\t{:08b}".format(self.flags)


class Cpu:
    """ Implements MOS 65XX series of CPUs, currently supports only 6510"""

    def __init__(self):
        self.rom_file = None
        self.model = (6, 5, 1, 0)
        self.ram = np.zeros(MOS_65XX_RAM_SIZE, dtype=np.uint8)
        self.op_table = opcode_table.opcodes()

        self.PC = np.dtype('<i2')  # Program Counter is a 16 bit register
        self.PC = MOS_65XX_RAM_START  # TODO: set this based on the input, e.g.. C64 files have start address as first 2 bytes
        self.S = np.uint8()  # Stack Pointer
        self.P = StatusRegister()  # CPU status flags
        self.A = np.uint8()  # Accumulator
        self.X = np.uint8()  # Index Register X
        self.Y = np.uint8()  # Index Register Y

    def nop(self,opcode):
        pass

    def lda(self,opcode):
        if opcode.mode == 'imm':
            self.A = self.ram[self.PC]
            self.PC += 1

    def jsr(self, opcode):
        # TODO implement stack push so we can return!
        # TODO: Move this to a get_two_byte_address_from ram type function?
        address = self.ram[self.PC:self.PC+2].tostring()
        address = int.from_bytes(address, byteorder='little')
        ###################################################################

        if address == 0xFFD2: # Fake the CHROUT Routine http://sta.c64.org/cbm64krnfunc.html
            sys.stdout.write(chr(self.A)),
            self.PC += 2
        else:
            self.PC = address
            print("Address:{0:00X}".format(self.PC))



    def step(self):

        # print(hex(self.PC))
        executing_opcode = self.op_table.lookup_hex_code(self.ram[self.PC])
        mnemonic = executing_opcode.mnemonic
        self.PC += 1
        methodToCall = getattr(self, mnemonic)
        result = methodToCall(executing_opcode)


    def load_prg(self):
        rom_file_name = "./ROMS/hello_world"
        with open(rom_file_name, "rb") as f:
            # Little endian read of the first two bytes
            # This gives the PC start address
            self.PC = struct.unpack('<H', f.read(2))[0]
            # Load the rest of the data into the rom_file and copy this to address space
            # TODO: Maybe optomise this a bit, and get rid of the copy
            self.rom_file = np.fromfile(f, dtype=np.uint8)
            np.copyto(self.ram[MOS_65XX_RAM_START:(MOS_65XX_RAM_START + self.rom_file.size)], self.rom_file, casting='equiv')


        # self.ram[MOS_65XX_RAM_START] = 0xEA
        # self.ram[0xC001] = 0xAE
        # self.PC = MOS_65XX_RAM_START


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)
    # print(hex(proc.PC))
    hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:0xC020])
    print("Loading PRG")
    proc.load_prg()
    print("Bytes Loaded:....")
    hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:MOS_65XX_RAM_START + proc.rom_file.size])
    # hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:0xC020])
    while(1):
        proc.step()

    # print("RAM Contents.........................")
    # hexdump.hexdump(proc.ram)


if __name__ == "__main__":
    main()
