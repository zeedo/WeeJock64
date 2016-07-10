import unittest
from unittest import TestCase

from cpu import Cpu as processor
test_cpu = processor()

class TestCpu(TestCase):
    def test_6510_ram_size(self):
        self.assertEqual(test_cpu.ram.size, 0xFFFF)


class TestStatusRegister(TestCase):
    def test_register_initialisation(self):
        self.assertTrue(test_cpu.P.interrupt)
        self.assertTrue(test_cpu.P.unused2)

        self.assertFalse(test_cpu.P.carry)
        self.assertFalse(test_cpu.P.zero)
        self.assertFalse(test_cpu.P.unused1)
        self.assertFalse(test_cpu.P.overflow)
        self.assertFalse(test_cpu.P.negative)
