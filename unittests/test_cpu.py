import unittest
from unittest import TestCase

from cpu import Cpu as processor


class TestCpu(TestCase):
    def test_6510_ram_size(self):
        test_cpu = processor()
        self.assertEqual(test_cpu.ram.size, 0xFFFF)


class TestStatusRegister(TestCase):
    def test_register_initialisation(self):
        test_cpu = processor()
        self.assertTrue(test_cpu.P.interrupt)
        self.assertTrue(test_cpu.P.unused2)

        self.assertFalse(test_cpu.P.carry)
        self.assertFalse(test_cpu.P.zero)
        self.assertFalse(test_cpu.P.unused1)
        self.assertFalse(test_cpu.P.overflow)
        self.assertFalse(test_cpu.P.negative)

    def test_get_set_flags(self):
        test_cpu = processor()
        test_cpu.P.flags = 0xFF
        self.assertTrue(test_cpu.P.interrupt)
        self.assertTrue(test_cpu.P.unused2)
        self.assertTrue(test_cpu.P.carry)
        self.assertTrue(test_cpu.P.zero)
        self.assertTrue(test_cpu.P.unused1)
        self.assertTrue(test_cpu.P.overflow)
        self.assertTrue(test_cpu.P.negative)

        self.assertEqual(test_cpu.P.flags, 0xFF)