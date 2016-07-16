import numpy as np


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
        return np.packbits([self.negative,
                            self.overflow,
                            self.unused,
                            self.breakflag,
                            self.decimal,
                            self.interrupt,
                            self.zero,
                            self.carry
                            ])[0]  # packbits returns an array but we only want the single element

    @flags.setter
    def flags(self, P):
        """Unpacks status flags from an int """
        self.carry, self.zero, self.interrupt, self.decimal, self.breakflag, self.unused, self.overflow, self.negative = np.unpackbits(
            np.asarray(P, dtype="uint8"))

    def __str__(self):
        return "Flags:\tNOuBDIZC\n\t\t{:08b}".format(self.flags)