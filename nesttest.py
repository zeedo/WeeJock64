import hexdump

from cpu import Cpu
import numpy as np


MOS_65XX_RAM_START = 0xC000
MOS_65XX_RAM_SIZE = 0xFFFF

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


def main():
    proc = Cpu()
    print("CPU Model: {0}".format(proc.model))
    print("CPU RAM Size: {0} ({0:X})".format(proc.ram.size))
    print(proc.P)
    # print(hex(proc.PC))
    print("\nLoading PRG.....\t", end=' ')
    load_nes_test(proc)
    print("Program Counter: " + hex(proc.PC),end='\t')
    print("Bytes Loaded:")
    # hexdump.hexdump(proc.ram[0:0xFFFF])
    # hexdump.hexdump(proc.ram[MOS_65XX_RAM_START:0xC020])
    while (1):
        print("A:{0:002x} X:{1:002x} Y:{2:002x} P:{3:002x} SP:N/A".format(proc.A,proc.X,proc.Y,proc.P.flags))
        proc.step()


if __name__ == "__main__":
    main()
