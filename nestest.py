import re
from typing import List

import numpy as np

from cpu import Cpu

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
        # sp_match = self.expected_sp == cpu.sp_reg
        # valid = pc_match and instruction_match and a_match and x_match and y_match and p_match and sp_match and data_bytes_match
        valid = pc_match and instruction_match and a_match and x_match and y_match and p_match

        if not valid:
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


        # self.ram[MOS_65XX_RAM_START] = 0xEA
        # self.ram[0xC001] = 0xAE
        # self.PC = MOS_65XX_RAM_START


with open('./ROMS/nestest.log', 'r') as nes_test_file:
    nes_test_log = NesTestLog(nes_test_file.readlines())

def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)
    # print(hex(proc.PC))

    print("\nLoading PRG.....\t", end=' ')
    load_nes_test(proc)
    print("Program Counter: " + hex(proc.PC), end='\t')
    print("Bytes Loaded:")
    # hexdump.hexdump(proc.ram[0:0xFFFF])
    # hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:0xC020])
    while 1:
        # print("A:{0:002x} X:{1:002x} Y:{2:002x} P:{3:002x} SP:N/A".format(proc.A, proc.X, proc.Y, proc.P.flags))
        proc.fetch()
        print("{0:X}\t{1}\tA:{2:002x} X:{3:002x} Y:{4:02x} P:{5:002x} SP:NA".format(proc.PC, proc.executing_opcode.mnemonic, proc.A, proc.X, proc.Y,
                                                                               proc.P.flags))
        print(proc.P)
        nes_test_log.compare(proc)
        proc.execute()



if __name__ == "__main__":
    main()
