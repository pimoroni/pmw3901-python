import pytest


def test_setup_cs_gpio(gpiod, gpiodevice, spidev, PAA5100):
    paa5100 = PAA5100(spi_cs_gpio=7)

    OUTL = gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)

    gpiodevice.get_pin.assert_called_with(7, f"{paa5100._device_name}_cs", OUTL)


def test_setup_bg_front(gpiod, gpiodevice, spidev, PAA5100):
    paa5100 = PAA5100(spi_cs_gpio=7)

    spidev.SpiDev().open.assert_called_with(0, 0)

    OUTL = gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)

    gpiodevice.get_pin.assert_called_with(7, f"{paa5100._device_name}_cs", OUTL)


def test_setup_bg_back(gpiod, gpiodevice, spidev, PAA5100):
    paa5100 = PAA5100(spi_cs_gpio=8)

    spidev.SpiDev().open.assert_called_with(0, 0)

    OUTL = gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)

    gpiodevice.get_pin.assert_called_with(8, f"{paa5100._device_name}_cs", OUTL)


def test_setup_not_present(gpiod, gpiodevice, spidev, PAA5100):
    spidev._fakedev.regs[0x00] = 0x00

    with pytest.raises(RuntimeError):
        PAA5100()
