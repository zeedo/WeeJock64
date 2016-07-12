import csv
from collections import namedtuple


class opcodes(object):
    def __init__(self, opcode_file='./data/6502-opcodes.csv'):
        self.op_table = {}
        self.csv_load_opcode_table(opcode_file)

    def csv_load_opcode_table(self, opcode_file):
        """Read in opcodes from a CSV file and creates a dict of lists with opcode hex value as key"""
        with open(opcode_file, 'r') as csvfile:
            csv_data = csv.reader(csvfile, delimiter=';', )
            for rows in csv_data:
                self.op_table[int(rows[0], 16)] = self.opcode_to_named_tuple(
                    rows[1:])  # first field in row is two characters in hex format, parse the rest as strings

    def lookup_hex_code(self, hex_code):
        try:
            return self.op_table[hex_code].mnemonic
        except KeyError:
            raise KeyError("Instruction not found: 0x{0:002X}".format(hex_code))

    @staticmethod
    def opcode_to_named_tuple(opcode):
        Opcode_tuple = namedtuple('Opcode_tuple', ['mnemonic', 'mode', 'cycles'])
        return Opcode_tuple(*opcode)


def main():
    op = opcodes()

    for hex_code, opcode in op.op_table.items():
        print("0x{0:002X}\t{1}\t\t{2: <8}{3}".format(hex_code, opcode.mnemonic, opcode.mode, opcode.cycles, ))


if __name__ == "__main__":
    main()
