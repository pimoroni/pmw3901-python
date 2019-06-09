import sys
import mock


class SPIDevFakeDevice():
    def __init__(self, bus=None, port=None):
        self.regs = [0 for _ in range(512)]
        self.regs[0x00] = 0x49  # Fake part ID
        self.regs[0x01] = 0x00  # Fake revision ID

    def open(self, bus, port):
        pass

    def xfer2(self, data):
        self.ptr = data[0]
        return [self.regs[self.ptr - 1 + x] for x in range(len(data))]


def test_setup():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    sys.modules['spidev'] = mock.Mock()
    sys.modules['spidev'].SpiDev = SPIDevFakeDevice
    from pmw3901 import PMW3901
    pmw3901 = PMW3901()
    del pmw3901

