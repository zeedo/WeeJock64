import re
from typing import List

from cpu import *

MOS_65XX_RAM_START = 0xC000
MOS_65XX_RAM_SIZE = 0xFFFF


class NesTestLog:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[NesTestLine]
        self.index = 0

        pattern = r'(.{4})\s*(.{9}).(.{4})(.{28})A:(.{2})\sX:(.{2})\sY:(.{2})\sP:(.{2})\sSP:(.{2})\sCYC:(.*)'
        compiled = re.compile(pattern)
        for line in lines:
            self.lines.append(NesTestLine(line, compiled))

    def compare(self, cpu):
        self.lines[self.index].compare(cpu)

        self.index += 1


class NesTestLine:
    """
    PC Bytes Instruction A X Y P SP CYC
    C000  4C F5 C5  JMP $C5F5                       A:00 X:00 Y:00 P:24 SP:FD CYC:  0
    """

    def __init__(self, line: str, compiled_pattern):
        self.line = line

        matches = compiled_pattern.match(self.line)

        self.expected_pc_reg = int(matches.group(1), 16)
        expected_data = matches.group(2)[3:].strip()
        if expected_data:
            self.expected_bytes = bytes([int(x, 16) for x in expected_data.split(' ')])
        else:
            self.expected_bytes = bytes()
        self.expected_instruction = matches.group(3).strip()
        self.expected_instruction_data = matches.group(4).strip()

        self.expected_a = int(matches.group(5), 16)
        self.expected_x = int(matches.group(6), 16)
        self.expected_y = int(matches.group(7), 16)
        self.expected_p = int(matches.group(8), 16)
        self.expected_sp = int(matches.group(9), 16)
        self.expected_cyc = int(matches.group(10))

    def compare(self, proc) -> bool:
        """
        checks a cpu against a log line
        """
        pc_match = self.expected_pc_reg == proc.PC
        instruction_match = self.expected_instruction in proc.executing_opcode.mnemonic.upper()
        a_match = self.expected_a == proc.A
        x_match = self.expected_x == proc.X
        y_match = self.expected_y == proc.Y
        p_match = self.expected_p == proc.P.flags
        sp_match = self.expected_sp == proc.SP
        valid = pc_match and instruction_match and a_match and x_match and y_match and p_match and sp_match
        if not valid:
            print(hex(proc.PC))
            raise Exception('Instruction results not expected\n{}'.format(proc.executing_opcode))


def load_nes_test(proc):
    # For now, you can load 0x4000 bytes starting at offset 0x0010, and map that as
    # ROM into both $8000-$BFFF and $C000-$FFFF of the emulated 6502's memory map.

    rom_file_name = "./ROMS/nestest.nes"
    with open(rom_file_name, "rb") as f:
        # Little endian read of the first two bytes
        # This gives the PC start address
        f.seek(16)

        proc.rom_file = np.fromfile(f, dtype=np.uint8)
        np.copyto(proc.ram[0xc000:(0xc000 + 0x3fff)], proc.rom_file[:0x3fff],
                  casting='equiv')
        np.copyto(proc.ram[0x8000:(0x8000 + 0x3fff)], proc.rom_file[:0x3fff],
                  casting='equiv')


with open('./ROMS/nestest.log', 'r') as nes_test_file:
    nes_test_log = NesTestLog(nes_test_file.readlines())


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)

    load_nes_test(proc)

    # Initialise stack register
    proc.SP = np.uint8(0xFD)

    while 1:
        proc.fetch()

        # *********************** Move to a disasm routine:
        if 'abs' == proc.executing_opcode.mode:
            high_byte = proc.ram[proc.PC + 2]
            low_byte = proc.ram[proc.PC + 1]
            high_byte <<= 8
            address = high_byte ^ low_byte
            opcode_size = 3

        elif 'imm' == proc.executing_opcode.mode:
            address = proc.PC + 1
            opcode_size = 2

        elif 'zp' == proc.executing_opcode.mode:
            address = proc.ram[proc.PC + 1]
            opcode_size = 2

        elif 'imp' == proc.executing_opcode.mode:
            address = None
            opcode_size = 1

        elif 'rel' == proc.executing_opcode.mode:
            address = proc.PC + 2 + proc.ram[proc.PC + 1]
            opcode_size = 2

        else:
            raise Exception("Address Mode Not Implemented {0}".format(proc.executing_opcode.mode))
        print("{:004X}\t".format(proc.PC), end="")
        print("{}".format(proc.executing_opcode.mnemonic.upper()), end="")
        if address:
            print(" {:004X}".format(address), end="")
        else:
            print("\t\t", end="")
        print("\tA:{:002x} X:{:002X} Y:{:002X} P:{:008b} SP:{:002X}".format(
            proc.A, proc.X, proc.Y, proc.P.flags, proc.SP))
        nes_test_log.compare(proc)
        proc.execute()


if __name__ == "__main__":
    main()
