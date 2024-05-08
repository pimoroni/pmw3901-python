1.0.0
-----

* Port to gpiod/gpiodevice
* Repackage to hatch/pyproject.toml
* BREAKING: spi_cs_gpio will not auto-detect SPI CS line, use spi_cs=(0, 1)
* BREAKING: Constants `BG_CS_FRONT_BCM` and `BG_CS_BACK_BCM` are now CS lines, not pins

0.1.0
-----

* Add init support for PAA5100JE
* Add frame capture support

0.0.1
-----

* Initial Release
