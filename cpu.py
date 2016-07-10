from pprint import pprint

import numpy as np

MOS_6510_RAM_SIZE = 0xFFFF


class StatusRegister:
    def __init__(self):
        # http://wiki.nesdev.com/w/index.php/CPU_status_flag_behavior
        self.carry = False  # Carry: 1 if last addition or shift resulted in a carry,
        # or if last subtraction resulted in no borrow
        self.zero = False  # Zero: 1 if last operation resulted in a 0 value
        self.interrupt = True  # Interrupt: Interrupt inhibit - interrupts are disabled if this is true!
        self.decimal = False  # Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
        self.unused1 = False  # No effect, used by the stack copy
        self.unused2 = True  # No effect, used by the stack copy
        self.overflow = False  # Overflow: 1 if last ADC or SBC resulted in signed overflow
        self.negative = False  # Negative: Set to bit 7 of the last operation


class Cpu:
    def __init__(self):
        self.model = (6, 5, 1, 0)
        self.ram = np.zeros(MOS_6510_RAM_SIZE, dtype=np.int8)

        self.PC = np.uint16()  # Program Counter is a 16 bit register
        self.S = np.uint8()  # Stack Pointer
        self.P = StatusRegister()  # CPU status flags
        self.A = np.uint8()  # Accumulator
        self.X = np.uint8()  # Index Register X
        self.Y = np.uint8()  # Index Register Y


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({1})".format(proc.ram.size, hex(proc.ram.size)))


if __name__ == "__main__":
    main()
