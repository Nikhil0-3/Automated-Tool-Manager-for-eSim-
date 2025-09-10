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
    """
    return shutil.which(tool_name) is not None

def add_to_path(path):
    """
    Add a directory to the system PATH environment variable
    """
    path_str = str(path)
    if path_str not in os.environ["PATH"]:
        os.environ["PATH"] = path_str + os.pathsep + os.environ["PATH"]
        logger.info(f"Added {path_str} to PATH (current session only)")

def create_directory(path):
    """
    Create a directory if it doesn't exist
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False