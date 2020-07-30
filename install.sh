set -e

ICEBOX_PATH=`dirname "$(readlink -f "$0")"`

# Set up the environment
echo "Creating Python virtual environment for Icebox..."
python3 -m venv "$ICEBOX_PATH/venv"
source "$ICEBOX_PATH/venv/bin/activate"
echo "Installing Python dependencies..."
pip install -r "$ICEBOX_PATH/requirements.txt"
deactivate

# Put the real user and path into the service file and install it.
sed -i".bak" "s,<user>,$USER,g ; s,<path>,$ICEBOX_PATH,g" "$ICEBOX_PATH/icebox.service"
sudo ln -s "$ICEBOX_PATH/icebox.service" "/etc/systemd/system/"
sudo systemctl enable icebox.service
sudo systemctl start icebox.service
echo "Created systemd icebox.service file and configured it to run on boot."
echo "icebox.service has been started. Installation successful!"