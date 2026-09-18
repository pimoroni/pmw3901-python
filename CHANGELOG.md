2.0.0
-----

* Enhancement: Repackage to the uv/hatchling method, with PyPI trusted publishing
* Enhancement: Version is derived from the git tag, __version__ from package metadata
* Python 3.9 or later, 3.7 and 3.8 support dropped

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
