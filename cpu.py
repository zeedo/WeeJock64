import struct

import hexdump
import numpy as np

import opcode_table
from instructions import Instructions
from statusregister import StatusRegister

MOS_65XX_RAM_START = 0xC000
MOS_65XX_RAM_SIZE = 0xFFFF
MOS_STACK_OFFSET = 0x100  # Stack grows down from here


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
        self.address_pointer = np.dtype('<i2')
        self.SP = np.uint8(0xFF)  # Stack Pointer
        self.P = StatusRegister()  # CPU status flags
        self.A = np.uint8()  # Accumulator
        self.X = np.uint8()  # Index Register X
        self.Y = np.uint8()  # Index Register Y

    def step(self):
        """ Perform a single CPU fetch execute cycle """
        self.fetch()
        self.execute()

    def fetch(self):
        """ Fetch next instruction from memory, lookup opcode and prepare to execute """

        self.executing_opcode = self.op_table.lookup_hex_code(self.ram[self.PC])

    def execute(self):
        """Execute fetched instructions by attempting to call a method in the CPU class using the opcode mnemonic
         As an attribute name """
        self.address_pointer = self.address_by_mode()

        if self.executing_opcode.mnemonic == 'and':  # and is a reserved keyword
            methodToCall = getattr(self, '_and')
        else:
            methodToCall = getattr(self, self.executing_opcode.mnemonic)
        result = methodToCall()

    def set_PC_bytes(self, high_byte, low_byte):
        """ Set Program Counter provided two bytes, helper function when reading bytes in little endian format """
        high_byte <<= 8

        self.PC = high_byte ^ low_byte

    def push(self, byte):
        """ Implementation of a stack push, place a byte at the current stack pointer and decrement the pointer
        Stack starts at MOS_STACK_OFFSET and grows down"""
        self.ram[MOS_STACK_OFFSET + self.SP] = byte
        self.SP -= 1  # Stack grows down

    def pop(self):
        """ Implementation of a stack pop, pop a byte at the current stack pointer and increment the pointer
        Stack starts at MOS_STACK_OFFSET and grows down"""
        self.SP += 1  # Stack grows down
        return self.ram[MOS_STACK_OFFSET + self.SP]

    def get_PC_bytes(self):
        """Get Program Counter bytes as a high and low byte, helper function when reading bytes in little endian format"""
        high_byte = self.PC & 0xFF00
        high_byte >>= 8
        low_byte = self.PC & 0x00FF
        return np.array([high_byte, low_byte], dtype=np.uint8)

    def address_by_mode(self):
        """Determine the appropriate address location of an instructions operand
        Returns the address required for instruction execution and increments the program counter appropriately"""

        if 'abs' == self.executing_opcode.mode:
            high_byte = self.ram[self.PC + 2]
            low_byte = self.ram[self.PC + 1]
            # print("high: {0:002X}, low: {1:002X}".format(high_byte,low_byte))
            high_byte <<= 8
            address = high_byte ^ low_byte
            self.PC += 3

        elif 'imm' == self.executing_opcode.mode:
            address = self.PC + 1
            self.PC += 2

        elif 'zp' == self.executing_opcode.mode:
            address = self.ram[self.PC + 1]
            self.PC += 2
        elif 'imp' == self.executing_opcode.mode:
            address = None
            self.PC += 1

        elif 'rel' == self.executing_opcode.mode:
            address = self.PC + 2 + np.int8(self.ram[self.PC + 1])
            self.PC += 2
        else:
            raise Exception("Address Mode Not Implemented {0}".format(self.executing_opcode.mode))

        return address

    def load_prg(self):
        """Placeholder function to load a PRG, will be replaced with command line file input
        Reads the first two bytes from a binary file and converts to an address
        Loads the rest of the file data at that address
        Sets the PC to the loaded address"""
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




def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))

    print("\nLoading PRG.....\t", end=' ')
    proc.load_prg()
    print("Program Counter: {:X}\n".format(proc.PC))
    print("Bytes Loaded:")
    hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:MOS_65XX_RAM_START + proc.rom_file.size])

    print("READY!\n\n")

    while (1):
        proc.step()


if __name__ == "__main__":
    main()
