Simple script for obtaining measurements from the INA226 sensor in Zabbix.  Based on [pi_ina226](https://github.com/e71828/pi_ina226) library.

Requires gpiod and SMBus2.
```
sudo apt-get install gpiod python3-smbus2
```
It is assumed that Zabbix-Agent is already installed.
Don't forget to grant the `zabbix` user the necessary permissions to work with I2C bus and GPIO.
 ```
 sudo usermod -a -G i2c zabbix
 groupadd gpio
 sudo usermod -a -G gpio zabbix
 ```
 ```
 sudo echo '# udev rules for gpio port access through libgpiod
SUBSYSTEM=="gpio", KERNEL=="gpiochip[0-4]", GROUP="gpio", MODE="0660"' > /etc/udev/rules.d/60-gpiod.rules

sudo udevadm trigger --subsystem-match=gpio
 ```
In `/etc/zabbix/zabbix_agentd.conf`, add the following UserParameter, modifying the path according to where the repository was cloned::
```
sudo echo 'UserParameter=data,python3 /opt/zabbix_ina226/get_data.py' >> /etc/zabbix/zabbix_agentd.conf
 ```
We can also obtain the GPIO state using the `get_gpio.sh` script and send the data to Zabbix. In this case, the sensor on GPIO 66 indicates the presence of AC power.
```
sudo echo 'UserParameter=ac_loss,bash /opt/zabbix_ina226/get_gpio.sh' >> /etc/zabbix/zabbix_agentd.conf
 ```
Let's restart the zabbix-agent to apply the changes.
 ```
sudo service zabbix-agent restart
```

The source code assumes that the sensor works with a 0.002R shunt, on the I2C-3 bus, and with the address 0x40. If not, you can change `shunt_ohms`, `busnum`, `address`, and `max_expected_amps` as needed in `get_data.py`.
