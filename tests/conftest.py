import sys
import mock
import pytest


class SPIDevFakeDevice():
    def __init__(self):
        self.regs = [0 for _ in range(512)]
        self.regs[0x00] = 0x49  # Fake part ID
        self.regs[0x01] = 0x00  # Fake revision ID

    def xfer2(self, data):
        self.ptr = data[0]
        return [self.regs[self.ptr - 1 + x] for x in range(len(data))]


@pytest.fixture(scope='function', autouse=False)
def PMW3901():
    from pmw3901 import PMW3901
    yield PMW3901
    del sys.modules['pmw3901']


@pytest.fixture(scope='function', autouse=False)
def PAA5100():
    from pmw3901 import PAA5100
    yield PAA5100
    del sys.modules['pmw3901']


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock spidev module."""
    fakedev = SPIDevFakeDevice()
    spidev = mock.MagicMock()
    spidev.SpiDev().xfer2.side_effect = fakedev.xfer2
    spidev._fakedev = fakedev
    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']


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
