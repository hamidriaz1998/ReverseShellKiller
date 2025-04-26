#!/bin/bash

# install.sh
INSTALL_DIR="/usr/local/bin"
SERVICE_DIR="/etc/systemd/system"
ENV_DIR="/etc/reverse-shell-killer"
ENV_FILE_TARGET="$ENV_DIR/environment"
ENV_FILE_SOURCE=".env" 

# Check if .env file exists
if [ ! -f "$ENV_FILE_SOURCE" ]; then
    echo "Error: .env file not found in the current directory."
    echo "Please create a .env file with your environment variables (GEMINI_API_KEY, EMAIL_USER, EMAIL_PASS, EMAIL_RECIPIENT) before running this script."
    exit 1
fi

# Copy binary
echo "Installing reverse-shell-killer to $INSTALL_DIR..."
SCRIPT_DIR=$(dirname "$0")
sudo cp "$SCRIPT_DIR/../dist/reverse-shell-killer" "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/reverse-shell-killer"

# Create environment directory
echo "Setting up environment file directory $ENV_DIR..."
sudo mkdir -p "$ENV_DIR"

# Copy environment file
echo "Copying $ENV_FILE_SOURCE to $ENV_FILE_TARGET..."
sudo cp "$ENV_FILE_SOURCE" "$ENV_FILE_TARGET"
sudo chmod 600 "$ENV_FILE_TARGET" # Set restrictive permissions

# Create systemd service file
echo "Setting up systemd service..."
# Note: Added --use-llm flag as env file likely contains API key
cat > reverse-shell-killer.service << EOF
[Unit]
Description=Reverse Shell Killer Service
After=network.target

[Service]
Type=simple
# Load environment variables from the file
EnvironmentFile=$ENV_FILE_TARGET
ExecStart=$INSTALL_DIR/reverse-shell-killer --interval 10 --logfile /var/log/reverse-shell-killer.log --use-llm
Restart=on-failure
RestartSec=5s
# Optional: Specify user/group if needed
# User=your_user
# Group=your_group

[Install]
WantedBy=multi-user.target
EOF

sudo mv reverse-shell-killer.service "$SERVICE_DIR/"

# Enable and start the service
echo "Enabling and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable reverse-shell-killer.service
sudo systemctl restart reverse-shell-killer.service # Use restart to ensure it picks up new env vars

echo "Installation completed! Service is running."
echo "Environment file copied to $ENV_FILE_TARGET."
echo "Check status with: sudo systemctl status reverse-shell-killer.service"
echo "View logs with: sudo journalctl -u reverse-shell-killer.service"
