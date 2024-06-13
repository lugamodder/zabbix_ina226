#!/usr/bin/env python3
import logging
from ina226 import INA226
from time import sleep
import json

busnum = 3
address = 0x40
max_expected_amps = 20
log_level = logging.CRITICAL
shunt_ohms=0.002
iterations = 1

if __name__ == "__main__":
    ina = INA226(
	address=address,
        busnum=busnum,
        max_expected_amps=max_expected_amps,
        log_level=log_level,
        shunt_ohms=shunt_ohms
    )

    ina.configure(avg_mode=2)
    #ina.set_low_battery(5)
    sleep(0.1)
    measurements = []
    bus_voltages = []
    bus_currents = []
    supply_voltages = []
    shunt_voltages = []
    powers = []

    for _ in range(iterations):  # Perform  measurements
        ina.wake()
        while True:
            if ina.is_conversion_ready():
                bus_voltages.append(ina.voltage())
                bus_currents.append(ina.current())
                supply_voltages.append(ina.supply_voltage())
                shunt_voltages.append(ina.shunt_voltage())
                powers.append(ina.power())
                sleep(0.1)
                break

 # Calculate average values
    avg_data = {
        "bus_voltage": round(sum(bus_voltages) / iterations, 3),
        "bus_current": round(sum(bus_currents) / iterations /1000, 3),
        "supply_voltage": round(sum(supply_voltages) / iterations, 3),
        "shunt_voltage": round(sum(shunt_voltages) / iterations, 3),
        "power": round(sum(powers) / iterations /1000, 3)
    }

    print(json.dumps(avg_data))
