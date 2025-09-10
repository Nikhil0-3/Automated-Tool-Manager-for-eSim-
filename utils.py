"""
Utility functions for the eSim Tool Manager
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from constants import SYSTEM
from logger import logger

def run_command(command, shell=True, check=True, capture_output=False, log_errors=True):
    """
    Run a system command and handle errors
    
    Args:
        command: Command to execute
        shell: Whether to use shell execution
        check: Whether to check return code
        capture_output: Whether to capture output
        log_errors: Whether to log errors if the command fails
    
    Returns:
        CompletedProcess object
    """
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=check, 
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if log_errors:
            logger.error(f"Command failed: {command}")
            logger.error(f"Error: {e}")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr.strip()}")
        return None
    except Exception as e:
        if log_errors:
            logger.error(f"Unexpected error executing command: {e}")
        return None

def is_tool_available(tool_name):
    """
    Check if a tool is available in the system PATH
    
    Args:
        tool_name: Name of the tool to check
    
    Returns:
        Boolean indicating if the tool is available
    """
    return shutil.which(tool_name) is not None

def get_linux_distro():
    """
    Get Linux distribution information
    
    Returns:
        Distribution name or None if not Linux
    """
    if SYSTEM != "linux":
        return None
        
    try:
        # Try to read /etc/os-release
        with open("/etc/os-release", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("ID="):
                    return line.split("=")[1].strip().strip('"')
    except Exception as e:
        logger.warning(f"Could not determine Linux distribution: {e}")
        
    return "unknown"

def add_to_path(path):
    """
    Add a directory to the system PATH environment variable
    
    Args:
        path: Path to add to PATH
    """
    path_str = str(path)
    if path_str not in os.environ["PATH"]:
        os.environ["PATH"] = path_str + os.pathsep + os.environ["PATH"]
        
        # For persistence, we might need to update shell config files
        # This is platform-specific and would require more complex handling
        logger.info(f"Added {path_str} to PATH (current session only)")

def create_directory(path):
    """
    Create a directory if it doesn't exist
    
    Args:
        path: Path to create
    
    Returns:
        Boolean indicating success
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False