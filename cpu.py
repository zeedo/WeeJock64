import hexdump
import numpy as np
import opcode_table


MOS_6510_RAM_SIZE = 0xFFFF


class StatusRegister(object):
    """MOS P Register, individual flags as booleans"""

    def __init__(self):
        # http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior

        self.carry = 0  # Carry: 1 if last addition or shift resulted in a carry,
        # or if last subtraction resulted in no borrow
        self.zero = 0  # Zero: 1 if last operation resulted in a 0 value
        self.interrupt = 1  # Interrupt: Interrupt inhibit - interrupts are disabled if this is true!
        self.decimal = 0  # Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
        self.unused1 = 0  # No effect, used by the stack copy
        self.unused2 = 1  # No effect, used by the stack copy
        self.overflow = 0  # Overflow: 1 if last ADC or SBC resulted in signed overflow
        self.negative = 0  # Negative: Set to bit 7 of the last operation


    @property
    def flags(self):
        """Packs all the status flags into a uint8 """
        return np.packbits([self.carry,
                            self.zero,
                            self.interrupt,
                            self.decimal,
                            self.unused1,
                            self.unused2,
                            self.overflow,
                            self.negative])[0]  # packbits returns an array but we only want the single element

    @flags.setter
    def flags(self, P):
        """Unpacks status flags from an int """
        self.carry, self.zero, self.interrupt, self.decimal, self.unused1, self.unused2, self.overflow, self.negative = np.unpackbits(
            np.asarray(P, dtype="uint8"))

    def __str__(self):
        return "Flags:\tCZIDuuON\n\t\t{:08b}".format(self.flags)


class Cpu:
    """ Implements MOS 65XX series of CPUs, currently supports only 6510"""

    def __init__(self):
        self.model = (6, 5, 1, 0)
        self.ram = np.zeros(MOS_6510_RAM_SIZE, dtype=np.int8)
        self.op_table = opcode_table.opcodes()

        self.PC = np.uint16()  # Program Counter is a 16 bit register
        self.S = np.uint8()  # Stack Pointer
        self.P = StatusRegister()  # CPU status flags
        self.A = np.uint8()  # Accumulator
        self.X = np.uint8()  # Index Register X
        self.Y = np.uint8()  # Index Register Y


    def nop(self):
        pass


    def step(self,instruction):
        try:
            methodToCall = getattr(self, instruction)
            result = methodToCall()
        except AttributeError as e:
                raise Exception("Instruction not implemented: {0}".format(instruction))


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)
    proc.step(proc.op_table.lookup_hex_code(0xEA))
    # print("RAM Contents.........................")
    # hexdump.hexdump(proc.ram)





if __name__ == "__main__":
    main()
