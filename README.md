# PMW3901 / PAA5100JE 2-Dimensional Optical Flow Sensor

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/pmw3901-python/test.yml?branch=main)](https://github.com/pimoroni/pmw3901-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/pmw3901-python/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/pmw3901-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/pmw3901.svg)](https://pypi.python.org/pypi/pmw3901)
[![Python Versions](https://img.shields.io/pypi/pyversions/pmw3901.svg)](https://pypi.python.org/pypi/pmw3901)


# Installing

Stable library from PyPi:

* Just run `python3 -m pip install pmw3901`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/pmw3901-python`
* `cd pmw3901-python`
* `./install.sh`

# Usage

The PAA5100JE has a slightly different init routine to the PMW3901, you should use the class provided to ensure it's set up correctly:

```
from pmw3901 import PAA5100
```

And for the PMW3901, continue using the old class:

```
from pmw3901 import PMW3901
```

The example `motion.py` demonstrates setting up either sensor, and accepts a `--board` argument to specify which you'd like to use.
