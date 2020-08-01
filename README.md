# Icebox

Icebox is a Python 3 program that monitors the temperature of the Raspberry Pi's system on chip and sets a GPIO pin to high when a temperature threshold is reached. When the temperature falls back below the threshold, the pin is set back to low. SoC temperature is monitored using Raspbian's [`vcgencmd`](https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md) utility.

Since the GPIO pins on the Pi are 3.3v and can only supply 16mA, this pin can be connected to a transistor or relay to switch on a higher-current or higher-voltage circuit that can power a fan.

The included install script will download the required dependencies and install a systemd service to run Icebox when the system boots. In [`__main__.py`](./__main__.py), the `MAX_TEMP` and `SIGNAL_PIN` constants can be changed to match your setup.