import sys

import mock
import pytest


class SPIDevFakeDevice:
    def __init__(self):
        self.regs = [0 for _ in range(512)]
        self.regs[0x00] = 0x49  # Fake part ID
        self.regs[0x01] = 0x00  # Fake revision ID

    def xfer2(self, data):
        self.ptr = data[0]
        return [self.regs[self.ptr - 1 + x] for x in range(len(data))]


@pytest.fixture(scope="function", autouse=False)
def PMW3901():
    from pmw3901 import PMW3901

    yield PMW3901
    del sys.modules["pmw3901"]


@pytest.fixture(scope="function", autouse=False)
def PAA5100():
    from pmw3901 import PAA5100

    yield PAA5100
    del sys.modules["pmw3901"]


@pytest.fixture(scope="function", autouse=False)
def spidev():
    """Mock spidev module."""
    fakedev = SPIDevFakeDevice()
    spidev = mock.MagicMock()
    spidev.SpiDev().xfer2.side_effect = fakedev.xfer2
    spidev._fakedev = fakedev
    sys.modules["spidev"] = spidev
    yield spidev
    del sys.modules["spidev"]


@pytest.fixture(scope='function', autouse=False)
def gpiod():
    sys.modules['gpiod'] = mock.Mock()
    sys.modules['gpiod.line'] = mock.Mock()
    yield sys.modules['gpiod']
    del sys.modules['gpiod.line']
    del sys.modules['gpiod']


@pytest.fixture(scope='function', autouse=False)
def gpiodevice():
    gpiodevice = mock.Mock()
    gpiodevice.get_pins_for_platform.return_value = [(mock.Mock(), 0), (mock.Mock(), 0)]
    gpiodevice.get_pin.return_value = (mock.Mock(), 0)

    sys.modules['gpiodevice'] = gpiodevice
    yield gpiodevice
    del sys.modules['gpiodevice']
