# Reverse Shell Killer

A security tool that automatically detects and terminates reverse shell connections on your system.

![Reverse Shell Killer](https://img.shields.io/badge/Security-Reverse%20Shell%20Killer-red)

## Features

- **Real-time monitoring** of processes for suspicious reverse shell connections
- **Advanced detection** using both pattern matching and LLM-based analysis 
- **Automatic termination** of detected malicious processes
- **Email notifications** when reverse shells are detected
- **Detailed logging** of all detection events
- **Low resource footprint** while running in the background

## Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/hamidriaz1998/ReverseShellKiller.git
cd ReverseShellKiller

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .
```

### Option 2: Using uv

If you don't have uv installed, you can get it from: https://github.com/astral-sh/uv

```bash
# Clone the repository
git clone https://github.com/hamidriaz1998/ReverseShellKiller.git
cd ReverseShellKiller

# Create a virtual environment with UV
uv init

# Install packages
uv sync
```

## Building a Linux ELF Binary

To build a standalone executable:

```bash
# Make sure you're in a virtual environment with dependencies installed
uv add pyinstaller

# Build the executable
pyinstaller --clean linux_build.spec

# Executable will be available at dist/reverse-shell-killer
```

## Usage

### Basic Usage

```bash
reverse-shell-killer
```

This will start the detector with default settings.

### Advanced Options

```bash
# Set custom scan interval (in seconds)
reverse-shell-killer --interval 5

# Specify log file location
reverse-shell-killer --logfile /var/log/revshell.log

# Test mode (detect but don't kill processes)
reverse-shell-killer --dry-run

# Enable LLM-based analysis (requires API key)
reverse-shell-killer --use-llm
```

### LLM-based Detection

For enhanced detection accuracy, the tool can use Google's Gemini API:

1. Get a Gemini API key from the [Google AI Studio](https://aistudio.google.com/)
2. Set it as an environment variable: `export GEMINI_API_KEY=your_key_here`
3. Run with LLM enabled: `reverse-shell-killer --use-llm`

## Email Notifications

To receive email notifications when reverse shells are detected:

1. Create a `.env` file with the following:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```
2. For Gmail, you'll need to create an [App Password](https://support.google.com/accounts/answer/185833)

## Running as a Service

For persistent protection, you can set up Reverse Shell Killer as a systemd service using two methods:

### Method 1: Using the installation script

Simply run the provided installation script:

```bash
# Make the script executable
chmod +x scripts/install_service.sh

# Run the installation script
sudo ./scripts/install_service.sh
```

### Method 2: Manual setup

If you prefer to set it up manually:

```bash
sudo nano /etc/systemd/system/reverse-shell-killer.service
```

Add the following configuration:

```ini
[Unit]
Description=Reverse Shell Killer Service
After=network.target

[Service]
Type=simple
ExecStart=/path/to/reverse-shell-killer --interval 10 --logfile /var/log/reverse-shell-killer.log
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reverse-shell-killer.service
sudo systemctl start reverse-shell-killer.service
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
