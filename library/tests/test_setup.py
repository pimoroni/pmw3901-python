import pytest


def test_setup(GPIO, spidev, PMW3901):
    pmw3901 = PMW3901()

    GPIO.setwarnings.assert_called_with(False)
    GPIO.setmode.assert_called_with(GPIO.BCM)
    GPIO.setup.assert_called_with(pmw3901.spi_cs_gpio, GPIO.OUT)


def test_setup_invalid_gpio(GPIO, spidev, PMW3901):
    pmw3901 = PMW3901(spi_cs_gpio=20)

    assert spidev.SpiDev.open.called_with(0, 0)

    del pmw3901


def test_setup_bg_front(GPIO, spidev, PMW3901):
    PMW3901(spi_cs_gpio=7)
    assert spidev.SpiDev.open.called_with(0, 1)


def test_setup_bg_back(GPIO, spidev, PMW3901):
    PMW3901(spi_cs_gpio=8)
    assert spidev.SpiDev.open.called_with(0, 0)


def test_setup_not_present(GPIO, spidev, PMW3901):
    spidev._fakedev.regs[0x00] = 0x00

    with pytest.raises(RuntimeError):
        PMW3901()
