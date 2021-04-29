import sys
import mock
import pytest


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


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""

    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock Spidev module."""

    spidev = mock.MagicMock()
    spidev.SpiDev = SPIDevFakeDevice

    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']
