#!/bin/bash

# Default values for service options
DEFAULT_INTERVAL=10
DEFAULT_LOGFILE="/var/log/reverse-shell-killer.log"
USE_LLM_FLAG="" # Empty means don't add the flag

# Parse command-line arguments for the installer script
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --interval) INTERVAL_ARG="$2"; shift ;;
        --logfile) LOGFILE_ARG="$2"; shift ;;
        --use-llm) USE_LLM_ARG="true" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Use provided arguments or defaults
SERVICE_INTERVAL=${INTERVAL_ARG:-$DEFAULT_INTERVAL}
SERVICE_LOGFILE=${LOGFILE_ARG:-$DEFAULT_LOGFILE}
if [[ "$USE_LLM_ARG" == "true" ]]; then
    USE_LLM_FLAG="--use-llm"
fi

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
# Ensure the binary exists before copying
BINARY_PATH="$SCRIPT_DIR/../dist/reverse-shell-killer"
if [ ! -f "$BINARY_PATH" ]; then
    echo "Error: Binary not found at $BINARY_PATH"
    echo "Please build the binary first using 'pyinstaller --clean linux_build.spec'"
    exit 1
fi
sudo cp "$BINARY_PATH" "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/reverse-shell-killer"

# Create environment directory
echo "Setting up environment file directory $ENV_DIR..."
sudo mkdir -p "$ENV_DIR"

# Copy environment file
echo "Copying $ENV_FILE_SOURCE to $ENV_FILE_TARGET..."
sudo cp "$ENV_FILE_SOURCE" "$ENV_FILE_TARGET"
sudo chmod 600 "$ENV_FILE_TARGET" # Set restrictive permissions

# Construct the ExecStart command dynamically
EXEC_START_CMD="$INSTALL_DIR/reverse-shell-killer --interval $SERVICE_INTERVAL --logfile $SERVICE_LOGFILE $USE_LLM_FLAG"
# Trim potential leading/trailing whitespace
EXEC_START_CMD=$(echo "$EXEC_START_CMD" | xargs)

echo "Service will run with command: $EXEC_START_CMD"

# Create systemd service file
echo "Setting up systemd service..."
cat > reverse-shell-killer.service << EOF
[Unit]
Description=Reverse Shell Killer Service
After=network.target

[Service]
Type=simple
# Load environment variables from the file
EnvironmentFile=$ENV_FILE_TARGET
ExecStart=$EXEC_START_CMD
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
