#!/usr/bin/env python3
import logging
from ina226 import INA226
from time import sleep
import json

busnum = 3
max_expected_amps = 20
log_level = logging.CRITICAL

def read():
    data = {
        "bus_voltage": round(ina.voltage(), 3),
        "bus_current": round((ina.current() / 1000), 3),
        "supply_voltage": round(ina.supply_voltage() ,3),
        "shunt_voltage": round(ina.shunt_voltage(), 3),
        "power": round((ina.power() / 1000), 3)
    }
    return json.dumps(data)

if __name__ == "__main__":
    ina = INA226(
        busnum=busnum,
        max_expected_amps=max_expected_amps,
        log_level=log_level
    )

    ina.configure()
    ina.set_low_battery(5)
    ina.wake(3)
    sleep(0.2)
    ina.wake(3)
    while 1:
        if ina.is_conversion_ready():
            json_result = read()
            print(json_result)
            break


