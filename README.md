# eSim Tool Manager

An automated tool manager for eSim that handles installation, configuration, update, and management of external tools and dependencies.

## Features

- **Tool Installation Management**: Download and install required external tools automatically
- **Update and Upgrade System**: Check for updates and upgrade installed tools
- **Configuration Handling**: Automate tool configuration and environment setup
- **Dependency Checker**: Verify and manage tool dependencies
- **Cross-Platform Support**: Works on Linux, Windows, and macOS
- **Package Manager Integration**: Uses system package managers (apt, Chocolatey, Homebrew)
- **User Interface**: Simple command-line interface for tool management

## Supported Tools

- Ngspice: Circuit simulator
- KiCad: EDA suite
- Xyce: Parallel circuit simulator



## Installation

Clone or download this repository

### 1. Prerequisites

*   **Git**: You must have Git installed to clone the repository.
*   **Python**: Ensure Python 3.8+ is installed and added to your system's PATH.

### 2. Environment Setup (Windows PowerShell)

These steps should be performed in a PowerShell terminal running as **Administrator**.

1.  **Open PowerShell as Administrator**:
    *   Search for "PowerShell" in the Start Menu.
    *   Right-click on "Windows PowerShell" and select "Run as administrator".

2.  **Set Execution Policy and Install Chocolatey**:
    Chocolatey is a package manager for Windows that this tool uses to install software like Ngspice. Run the following command to set the necessary execution policy and install Chocolatey:
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```
    *Note: After installation, you may need to close and reopen your Administrator PowerShell window for the `choco` command to be available.*

### 3. Project Setup

1.  **Clone the Repository**:
    Navigate to your desired directory and clone the project from GitHub.
    ```powershell
    git clone <your-repository-url>
    cd tool # Or your repository's folder name
    ```

2.  **Create and Activate a Python Virtual Environment**:
    This isolates the project's dependencies from your system's Python installation.
    ```powershell
    # Create the virtual environment
    python -m venv .venv

    # Activate the virtual environment
    .\.venv\Scripts\Activate.ps1
    ```
    Your prompt should now be prefixed with `(.venv)`, indicating the virtual environment is active.

3.  **Install Dependencies**:
    Install the required Python packages listed in `requirements.txt`.
    ```powershell
    pip install -r requirements.txt
    ```

## Usage

With the setup complete, you can now use the tool manager from your activated virtual environment.

*   **List all available tools and their status**:
    ```powershell
    python main.py list
    ```

*   **Install a tool (e.g., ngspice)**:
    The manager will check for and offer to install any missing dependencies first.
    ```powershell
    python main.py install ngspice
    ```

*   **Check for available updates for installed tools**:
    ```powershell
    python main.py update
    ```
