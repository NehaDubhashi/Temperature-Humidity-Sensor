import smbus2
import time

# constants for AHT10
AHT10_ADDRESS = 0x38
AHT10_INIT_CMD = 0xE1
AHT10_MEASURE_CMD = 0xAC
AHT10_RESET_CMD = 0xBA

# initializing I2C
bus = smbus2.SMBus(1)

def aht10_init():
    bus.write_i2c_block_data(AHT10_ADDRESS, AHT10_INIT_CMD, [0x08, 0x00])
    time.sleep(1)

def aht10_reset():
    bus.write_byte(AHT10_ADDRESS, AHT10_RESET_CMD)
    time.sleep(1)

def aht10_measure():
    bus.write_i2c_block_data(AHT10_ADDRESS, AHT10_MEASURE_CMD, [0x33, 0x00])
    data = bus.read_i2c_block_data(AHT10_ADDRESS, 0x00, 6)
    time.sleep(1)

    og_humidity = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
    og_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

    humidity = og_humidity * 100 / 1048576.0
    temperature = og_temperature * 200 / 1048576.0 - 50

    return temperature, humidity

# initializing and resetting the sensor
aht10_reset()
aht10_init()

while True:
        # measures temperature and humidity
        temperature, humidity = aht10_measure()

        if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature:.2f} °C")
                print(f"Humidity: {humidity:.2f} %")

        time.sleep(10)
