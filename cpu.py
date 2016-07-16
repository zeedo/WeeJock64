import struct

import hexdump
import numpy as np

import opcode_table
from instructions import Instructions

from statusregister import StatusRegister

MOS_65XX_RAM_START = 0xC000
MOS_65XX_RAM_SIZE = 0xFFFF


class Cpu(Instructions):
    """ Implements MOS 65XX series of CPUs, currently supports only 6510"""

    def __init__(self):
        self.rom_file = None
        self.model = (6, 5, 1, 0)
        self.ram = np.zeros(MOS_65XX_RAM_SIZE, dtype=np.uint8)
        self.op_table = opcode_table.opcodes()
        self.executing_opcode = None

        self.PC = np.dtype('<i2')  # Program Counter is a 16 bit register
        self.PC = MOS_65XX_RAM_START  # TODO: set this based on the input, e.g.. C64 files have start address as first 2 bytes
        self.PC_fake_retaddr = np.dtype('<i2')  # Fake return address until we implement a stack
        self.S = np.uint8()  # Stack Pointer
        self.P = StatusRegister()  # CPU status flags
        self.A = np.uint8()  # Accumulator
        self.X = np.uint8()  # Index Register X
        self.Y = np.uint8()  # Index Register Y

    def step(self):

        # FETCH
        self.executing_opcode = self.op_table.lookup_hex_code(self.ram[self.PC])
        self.address_pointer = self.address_by_mode()
        self.PC += 1

        # EXECUTE
        methodToCall = getattr(self, self.executing_opcode.mnemonic)
        result = methodToCall()

    def set_PC_bytes(self, high_byte, low_byte):
        high_byte <<= 8

        self.PC = high_byte ^ low_byte

    def get_PC_Bytes(self):
        high_byte = self.PC & 0xFF00
        high_byte >>= 8
        low_byte = self.PC & 0x00FF
        return np.array([high_byte, low_byte], dtype=np.uint8)

    def address_by_mode(self):

        if 'abs' in self.executing_opcode.mode:
            high_byte = self.ram[self.PC + 2]
            low_byte = self.ram[self.PC + 1]
            # print("high: {0:002X}, low: {1:002X}".format(high_byte,low_byte))
            high_byte <<= 8
            address = high_byte ^ low_byte
            self.PC += 2

        elif 'imm' in self.executing_opcode.mode:
            address = self.PC + 1
            self.PC = address
        else:
            address = None

        return address

    def load_prg(self):
        rom_file_name = "./ROMS/hello_world.prg"
        with open(rom_file_name, "rb") as f:
            # Little endian read of the first two bytes
            # This gives the PC start address
            self.PC = struct.unpack('<H', f.read(2))[0]
            # Load the rest of the data into the rom_file and copy this to address space
            # TODO: Maybe optomise this a bit, and get rid of the copy
            # TODO: When moving this to a ROM loader file think about whether we load and execute separately
            self.rom_file = np.fromfile(f, dtype=np.uint8)
            np.copyto(self.ram[self.PC:(self.PC + self.rom_file.size)], self.rom_file,
                      casting='equiv')


            # self.ram[MOS_65XX_RAM_START] = 0xEA
            # self.ram[0xC001] = 0xAE
            # self.PC = MOS_65XX_RAM_START


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)
    # print(hex(proc.PC))
    print("\nLoading PRG.....\t", end=' ')
    proc.load_prg()
    print("Program Counter: " + hex(proc.PC), end='\t')
    print("Bytes Loaded:")
    hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:MOS_65XX_RAM_START + proc.rom_file.size])
    # hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:0xC020])
    while (1):
        proc.step()
        # print("A:{0:002x} X:{0:002x} Y:{0:002x} P:{0:002x} SP:{0:002x}".format(proc.A,proc.X,proc.Y,proc.P))


        # print("RAM Contents.........................")
        # hexdump.hexdump(proc.ram)


if __name__ == "__main__":
    main()
