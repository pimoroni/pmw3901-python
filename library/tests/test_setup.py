def test_setup_pwm3901(spidev, GPIO):
    from pmw3901 import PMW3901
    pmw3901 = PMW3901()
    del pmw3901


def test_setup_paa5100(spidev, GPIO):
    from pmw3901 import PAA5100
    paa5100 = PAA5100()
    del paa5100
