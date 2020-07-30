# Icebox

Icebox is a Python program that monitors the temperature of the Raspberry Pi's system on chip via `vcgencmd` and sets a GPIO pin to high when the temperature threshold is reached. When the temperature falls back below the threshold, the pin is set back to low.

Since the GPIO pins on the Pi are 3.3v and can only supply 16mA, this pin can be connected to a transistor or relay to switch on a higher current or higher voltage circuit that can power a fan.

The included install script will download the dependencies and install a systemd service to run Icebox when the system boots.