#!/bin/bash

# install.sh
INSTALL_DIR="/usr/local/bin"
SERVICE_DIR="/etc/systemd/system"

# Copy binary
echo "Installing reverse-shell-killer to $INSTALL_DIR..."
sudo cp dist/reverse-shell-killer $INSTALL_DIR/
sudo chmod +x $INSTALL_DIR/reverse-shell-killer

# Create systemd service file
echo "Setting up systemd service..."
cat > reverse-shell-killer.service << EOF
[Unit]
Description=Reverse Shell Killer Service
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_DIR/reverse-shell-killer --interval 10 --logfile /var/log/reverse-shell-killer.log
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

sudo mv reverse-shell-killer.service $SERVICE_DIR/

# Enable and start the service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable reverse-shell-killer.service
sudo systemctl start reverse-shell-killer.service

echo "Installation completed! Service is running."
echo "Check status with: sudo systemctl status reverse-shell-killer.service"
echo "View logs with: sudo journalctl -u reverse-shell-killer.service"
