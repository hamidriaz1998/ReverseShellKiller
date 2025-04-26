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

## Email Notifications & LLM API Key

To receive email notifications and/or use LLM-based detection, you need to configure environment variables.

**Before running the installation script or starting the service manually**, create a file named `.env` in the root directory of this project with the following content, filling in your actual details:

```dotenv
# .env file content
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_RECIPIENT=recipient_email@example.com
```

*   **GEMINI_API_KEY:** Your API key from [Google AI Studio](https://aistudio.google.com/). Required if using `--use-llm`.
*   **EMAIL_USER:** Your Gmail address used for sending notifications.
*   **EMAIL_PASS:** A Gmail [App Password](https://support.google.com/accounts/answer/185833). **Do not use your regular Gmail password.**
*   **EMAIL_RECIPIENT:** The email address where notifications should be sent.

**Important:** Keep this `.env` file secure and do not commit it to version control (it's included in `.gitignore`).

## Running as a Service

For persistent protection, you can set up Reverse Shell Killer as a systemd service.

### Method 1: Using the installation script (Recommended)

1.  **Build the binary:** Follow the steps in "Building a Linux ELF Binary".
2.  **Create the `.env` file:** Ensure the `.env` file exists in the project's root directory with your credentials as described above.
3.  **Run the script:**
    ```bash
    # Make the script executable (if needed)
    chmod +x scripts/install_service.sh

    # Run the installation script from the project root directory
    sudo ./scripts/install_service.sh
    ```
    This script will:
    *   Copy the built binary to `/usr/local/bin/`.
    *   Copy your `.env` file to `/etc/reverse-shell-killer/environment` and set secure permissions.
    *   Create and enable a systemd service (`reverse-shell-killer.service`) configured to use the environment file and the `--use-llm` flag.
    *   Start the service.

### Method 2: Manual setup

1.  **Build the binary** and place it somewhere accessible (e.g., `/usr/local/bin/reverse-shell-killer`).
2.  **Create the environment file:** Manually create the directory `/etc/reverse-shell-killer` and copy your `.env` file to `/etc/reverse-shell-killer/environment`. Set permissions: `sudo chmod 600 /etc/reverse-shell-killer/environment`.
3.  **Create the service file:**
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
    # Load environment variables
    EnvironmentFile=/etc/reverse-shell-killer/environment
    # Run with LLM enabled, adjust path and flags as needed
    ExecStart=/usr/local/bin/reverse-shell-killer --interval 10 --logfile /var/log/reverse-shell-killer.log --use-llm
    Restart=on-failure
    RestartSec=5s
    # Optional: Specify user/group if needed
    # User=your_user
    # Group=your_group

    [Install]
    WantedBy=multi-user.target
    ```
4.  **Enable and start the service:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable reverse-shell-killer.service
    sudo systemctl start reverse-shell-killer.service
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
