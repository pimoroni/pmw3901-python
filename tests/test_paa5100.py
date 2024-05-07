import pytest


def test_setup(GPIO, spidev, PAA5100):
    paa5100 = PAA5100()

    GPIO.setwarnings.assert_called_with(False)
    GPIO.setmode.assert_called_with(GPIO.BCM)
    GPIO.setup.assert_called_with(paa5100.spi_cs_gpio, GPIO.OUT)


def test_setup_invalid_gpio(GPIO, spidev, PAA5100):
    paa5100 = PAA5100(spi_cs_gpio=20)

    spidev.SpiDev().open.assert_called_with(0, 0)

    del paa5100


def test_setup_bg_front(GPIO, spidev, PAA5100):
    PAA5100(spi_cs_gpio=7)
    spidev.SpiDev().open.assert_called_with(0, 1)


def test_setup_bg_back(GPIO, spidev, PAA5100):
    PAA5100(spi_cs_gpio=8)
    spidev.SpiDev().open.assert_called_with(0, 0)


def test_setup_not_present(GPIO, spidev, PAA5100):
    spidev._fakedev.regs[0x00] = 0x00

    with pytest.raises(RuntimeError):
        PAA5100()
