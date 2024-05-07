import pytest


def test_setup(gpiod, gpiodevice, spidev, PMW3901):
    pmw3901 = PMW3901()

    OUTL = gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)

    gpiodevice.get_pin.assert_called_with(7, f"{pmw3901._device_name}_cs", OUTL)


def test_setup_invalid_gpio(gpiod, gpiodevice, spidev, PMW3901):
    pmw3901 = PMW3901(spi_cs_gpio=20)

    spidev.SpiDev().open.assert_called_with(0, 0)

    del pmw3901


def test_setup_bg_front(gpiod, gpiodevice, spidev, PMW3901):
    PMW3901(spi_cs_gpio=7)
    spidev.SpiDev().open.assert_called_with(0, 1)


def test_setup_bg_back(gpiod, gpiodevice, spidev, PMW3901):
    PMW3901(spi_cs_gpio=8)
    spidev.SpiDev().open.assert_called_with(0, 0)


def test_setup_not_present(gpiod, gpiodevice, spidev, PMW3901):
    spidev._fakedev.regs[0x00] = 0x00

    with pytest.raises(RuntimeError):
        PMW3901()
