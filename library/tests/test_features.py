import pytest
import struct


def test_get_motion_timeout(GPIO, spidev, PMW3901):
    pmw3901 = PMW3901()

    with pytest.raises(RuntimeError):
        pmw3901.get_motion(timeout=0.1)


def test_get_motion(GPIO, spidev, PMW3901):
    pmw3901 = PMW3901()

    spidev._fakedev.regs[0x15:0x15 + 12] = list(
        struct.pack(
            "<BBBhhBBBBBB",
            0,             # _
            0b10000000,    # dr
            0,             # obs
            -50,           # x
            99,            # y
            0x20,          # quality
            0,             # raw_sum
            0,             # raw_max
            0,             # raw_min
            0,             # shutter_upper
            0              # shutter_lower
        )
    )

    x, y = pmw3901.get_motion(timeout=0.1)

    assert (x, y) == (-50, 99)
