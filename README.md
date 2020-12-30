# Icebox

Icebox is a Python 3 program that monitors the temperature of the Raspberry Pi's system on chip and sets a GPIO pin to high when a temperature threshold is reached. When the temperature falls back below the threshold, the pin is set back to low. SoC temperature is monitored using Raspbian's [`vcgencmd`](https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md) utility.

Since the GPIO pins on the Pi are 3.3v and can only supply 16mA, this pin can be connected to a transistor or relay to switch on a higher-current or higher-voltage circuit that can power a fan.

## Usage

In [`__main__.py`](./__main__.py), the `MAX_TEMP` and `SIGNAL_PIN` constants can be changed to match your setup.

### Systemd

The included `install.sh` script will download the required dependencies in a Python 3 virtual environment and will install a systemd service to run Icebox when the system boots. The user that runs the script will be used as the user for the systemd service. This user must belong to the `video` and `gpio` groups.

### Docker

Alternatively, Icebox can run inside a container. To build the container, run the following command from within the Icebox directory:
```Shell
docker build -t icebox .
```

The container will need access to the `gpiomem` and `vchiq` devices to access the GPIO pins and to interface with the VideoCore hardware, which is necessary to read the SoC temperature.

The VideCore directory `/opt/vc` will need to be shared, along with the symlink to `vcgencmd` which is located in `/usr/bin` on Raspberry Pi OS/Raspbian.

Finally, the container will need `/opt/vc/lib` added to its library path in order to load libs necessary for the `vcgencmd` utility.

```Shell
docker run --device /dev/gpiomem \ 
           --device /dev/vchiq \
           -v /opt/vc:/opt/vc \
           -v /usr/bin/vcgencmd:/usr/bin/vcgencmd \
           --env LD_LIBRARY_PATH=/opt/vc/lib \
           icebox
```

It is best to run the container as a non-root user. To do this, the container will need to be added to the `video` and `gpio` groups:

```Shell
docker run --device /dev/gpiomem \
           --device /dev/vchiq \
           -v /opt/vc:/opt/vc \
           -v /usr/bin/vcgencmd:/usr/bin/vcgencmd \
           --env LD_LIBRARY_PATH=/opt/vc/lib \
           --user <non-root UID> \
           --group-add <video GID> \
           --group-add <gpio GID> \
           icebox
```
