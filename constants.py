"""
Constants and definitions for the eSim Tool Manager
"""

import platform
from pathlib import Path

# System information
SYSTEM = platform.system().lower()
ARCHITECTURE = platform.machine()

# Supported platforms
PLATFORMS = {
    "linux": ["ubuntu", "debian", "fedora", "centos"],
    "windows": ["windows10", "windows11"],
    "darwin": ["macos"]
}

# Package managers
PACKAGE_MANAGERS = {
    "linux": {
        "ubuntu": "apt-get",
        "debian": "apt-get",
        "fedora": "dnf",
        "centos": "yum"
    },
    "windows": "choco",
    "darwin": "brew"
}

# Default installation paths
DEFAULT_PATHS = {
    "linux": Path.home() / "esim-tools",
    "windows": Path("C:\\") / "esim-tools",
    "darwin": Path.home() / "esim-tools"
}

# Configuration file
CONFIG_FILE = "tools_config.json"
USER_CONFIG_FILE = "user_config.json"

# Log file
LOG_FILE = "esim_tool_manager.log"