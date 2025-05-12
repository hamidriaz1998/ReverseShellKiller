#!/bin/bash

# Paths
INSTALL_DIR="/usr/local/bin"
SERVICE_DIR="/etc/systemd/system"
ENV_DIR="/etc/reverse-shell-killer"
SERVICE_NAME="reverse-shell-killer.service"
BINARY_NAME="reverse-shell-killer"

echo "Uninstalling Reverse Shell Killer..."

# Stop and disable the service
echo "Stopping and disabling service..."
sudo systemctl stop $SERVICE_NAME 2>/dev/null
sudo systemctl disable $SERVICE_NAME 2>/dev/null
sudo systemctl daemon-reload

# Remove service file
echo "Removing service file..."
if [ -f "$SERVICE_DIR/$SERVICE_NAME" ]; then
    sudo rm "$SERVICE_DIR/$SERVICE_NAME"
    echo "Service file removed."
else
    echo "Service file not found, skipping."
fi

# Remove binary
echo "Removing binary..."
if [ -f "$INSTALL_DIR/$BINARY_NAME" ]; then
    sudo rm "$INSTALL_DIR/$BINARY_NAME"
    echo "Binary removed."
else
    echo "Binary not found, skipping."
fi

# Remove environment directory and files
echo "Removing environment directory and files..."
if [ -d "$ENV_DIR" ]; then
    sudo rm -rf "$ENV_DIR"
    echo "Environment directory removed."
else
    echo "Environment directory not found, skipping."
fi

echo "Uninstallation completed successfully!"
echo "Note: Any log files created by the service have not been removed."
echo "Log files might be located at the path specified during installation."
