import time
import struct
import spidev
from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import LookupAdapter, Adapter
import RPi.GPIO as GPIO

WAIT = -1

BG_CS_FRONT_BCM = 7
BG_CS_BACK_BCM = 8

class S16Adapter(Adapter):
    """Convert from bytes to a signed 16bit integer."""

    def _decode(self, value):
        return struct.unpack('<h', _int_to_bytes(value, 2))[0]


class SPItoI2CDevice():
    def __init__(self, spi_device, spi_cs_gpio):
        self.spi = spi_device
        self.spi_cs_gpio = spi_cs_gpio

    def write_i2c_block_data(self, address, register, values):
        for offset, value in enumerate(values):
            GPIO.output(self.spi_cs_gpio, 0)
            self.spi.xfer2([(register + offset) | 0x80, value])
            GPIO.output(self.spi_cs_gpio, 1)

    def read_i2c_block_data(self, address, register, length):
        result = []
        for x in range(length):
            GPIO.output(self.spi_cs_gpio, 0)
            value = self.spi.xfer2([register + x, 0])
            GPIO.output(self.spi_cs_gpio, 1)
            # print("SPI READ: ", value)
            result.append(value[1])

        return result


class PMW3901():
    def __init__(self, spi_port=0, spi_cs=1, spi_cs_gpio=BG_CS_FRONT_BCM):
        self.spi_cs_gpio = spi_cs_gpio
        self.spi_dev = spidev.SpiDev()
        self.spi_dev.open(spi_port, spi_cs)
        self.spi_dev.max_speed_hz = 400000
        self.spi_dev.no_cs = True

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.spi_cs_gpio, GPIO.OUT)
        GPIO.output(self.spi_cs_gpio, 1)

        self._secret_sauce()

        self._pwm3901 = Device([0x00], i2c_dev=SPItoI2CDevice(self.spi_dev, self.spi_cs_gpio), bit_width=8, registers=(
            Register('ID', 0x00, fields=(
                BitField('product_id', 0xFF00),
                BitField('revision_id', 0x00FF)
            ), bit_width=16),
            Register('MOTION', 0x02, fields=(
                BitField('data_ready', 0x8000000000),
                BitField('delta_x', 0x00FFFF0000, adapter=S16Adapter()),
                BitField('delta_y', 0x000000FFFF, adapter=S16Adapter())
            ), bit_width=40)
        ))

        with self._pwm3901.ID as ID:
            product_id = ID.get_product_id()
            revision = ID.get_revision_id()
            if product_id != 0x49 or revision != 0x00:
                raise RuntimeError("Invalid Product ID or Revision for PMW3901: 0x{:02x}/0x{:02x}".format(product_id, revision))
            # print("Product ID: {}".format(ID.get_product_id()))
            # print("Revision: {}".format(ID.get_revision_id()))

    def get_motion(self):
        for x in range(10):
            with self._pwm3901.MOTION as MOTION:
                if not MOTION.get_data_ready():
                    continue
                return MOTION.get_delta_x(), MOTION.get_delta_y()
            time.sleep(0.001)

        return 0, 0

    def _write(self, register, value):
        GPIO.output(7, 0)
        self.spi_dev.xfer2([register | 0x80, value])
        GPIO.output(7, 1)

    def _read(self, register):
        GPIO.output(7, 0)
        result = self.spi_dev.xfer2([register, 0])
        GPIO.output(7, 1)
        return result[1]

    def _bulk_write(self, data):
        for x in range(0, len(data), 2):
            register, value = data[x:x+2]
            if register == WAIT:
                # print("Sleeping for: {:02d}ms".format(value))
                time.sleep(value / 1000)
            else:
                # print("Writing: {:02x} to {:02x}".format(register, value))
                self._write(register, value)

    def _secret_sauce(self):
        """Write the secret sauce registers.
        
        Don't ask what these do, the datasheet refuses to explain.
        
        They are some proprietary calibration magic.

        """
        self._bulk_write([
            0x7f, 0x00,
            0x55, 0x01,
            0x50, 0x07,

            0x7f, 0x0e,
            0x43, 0x10
        ])
        if self._read(0x67) & 0b10000000:
            self._write(0x48, 0x04)
        else:
            self._write(0x48, 0x02)
        self._bulk_write([
            0x7f, 0x00,
            0x51, 0x7b,

            0x50, 0x00,
            0x55, 0x00,
            0x7f, 0x0E
        ])
        if self._read(0x73) == 0x00:
            c1 = self._read(0x70)
            c2 = self._read(0x71)
            if c1 <= 28:
                c1 += 14
            if c1 > 28:
                c1 += 11
            c1 = max(0, min(0x3F, c1))
            c2 = (c2 * 45) // 100
            self._bulk_write([
                0x7f, 0x00,
                0x61, 0xad,
                0x51, 0x70,
                0x7f, 0x0e
            ])
            self._write(0x70, c1)
            self._write(0x71, c2)
        self._bulk_write([
            0x7f, 0x00,
            0x61, 0xad,
            0x7f, 0x03,
            0x40, 0x00,
            0x7f, 0x05,

            0x41, 0xb3,
            0x43, 0xf1,
            0x45, 0x14,
            0x5b, 0x32,
            0x5f, 0x34,
            0x7b, 0x08,
            0x7f, 0x06,
            0x44, 0x1b,
            0x40, 0xbf,
            0x4e, 0x3f,
            0x7f, 0x08,
            0x65, 0x20,
            0x6a, 0x18,

            0x7f, 0x09,
            0x4f, 0xaf,
            0x5f, 0x40,
            0x48, 0x80,
            0x49, 0x80,

            0x57, 0x77,
            0x60, 0x78,
            0x61, 0x78,
            0x62, 0x08,
            0x63, 0x50,
            0x7f, 0x0a,
            0x45, 0x60,
            0x7f, 0x00,
            0x4d, 0x11,

            0x55, 0x80,
            0x74, 0x21,
            0x75, 0x1f,
            0x4a, 0x78,
            0x4b, 0x78,

            0x44, 0x08,
            0x45, 0x50,
            0x64, 0xff,
            0x65, 0x1f,
            0x7f, 0x14,
            0x65, 0x67,
            0x66, 0x08,
            0x63, 0x70,
            0x7f, 0x15,
            0x48, 0x48,
            0x7f, 0x07,
            0x41, 0x0d,
            0x43, 0x14,

            0x4b, 0x0e,
            0x45, 0x0f,
            0x44, 0x42,
            0x4c, 0x80,
            0x7f, 0x10,

            0x5b, 0x02,
            0x7f, 0x07,
            0x40, 0x41,
            0x70, 0x00,
            WAIT, 0x0A,  # Sleep for 10ms   

            0x32, 0x44,
            0x7f, 0x07,
            0x40, 0x40,
            0x7f, 0x06,
            0x62, 0xf0,
            0x63, 0x00,
            0x7f, 0x0d,
            0x48, 0xc0,
            0x6f, 0xd5,
            0x7f, 0x00,

            0x5b, 0xa0,
            0x4e, 0xa8,
            0x5a, 0x50,
            0x40, 0x80,
            WAIT, 0xF0,

            0x7f, 0x14,  # Enable LED_N pulsing
            0x6f, 0x1c,
            0x7f, 0x00
        ])

if __name__ == "__main__":
    flo = PMW3901(spi_port=0, spi_cs=1)
    try:
        while True:
            x, y = flo.get_motion()
            print("Motion: {:06d} {:06d}".format(x, y))
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
