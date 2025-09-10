"""
Tool installation functionality for the eSim Tool Manager
"""

import ctypes
import os
import platform
import tempfile
from pathlib import Path
from typing import Dict, Any, Tuple, List

from utils import run_command, create_directory, add_to_path
from config_manager import ConfigManager
from dependency_checker import DependencyChecker
from logger import logger

class InstallManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.dependency_checker = DependencyChecker()
    
    def install_tool(self, tool_name: str) -> Tuple[bool, str]:
        """
        Install a tool
        
        Args:
            tool_name: Name of the tool to install
        
        Returns:
            Tuple of (success status, message)
        """
        # On Windows, check for admin rights if choco is used, as it's often required.
        if platform.system().lower() == "windows":
            try:
                is_admin = (os.getuid() == 0)
            except AttributeError:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            
            if not is_admin and self.dependency_checker.available_package_manager == "choco":
                return False, "Administrator privileges are required to install tools with Chocolatey. Please run the terminal as an administrator."

        # Get tool configuration
        tool_config = self.config_manager.get_tool_config(tool_name)
        if not tool_config:
            return False, f"Tool {tool_name} not found in configuration"
        
        # Check if already installed
        if self.is_tool_installed(tool_name, tool_config):
            return True, f"Tool {tool_name} is already installed"
        
        # Check dependencies
        dep_success, missing_deps = self.dependency_checker.check_tool_dependencies(tool_config)
        if not dep_success and missing_deps:
            install_deps = self.prompt_install_dependencies(missing_deps)
            if install_deps:
                success = self.dependency_checker.install_system_dependencies(missing_deps)
                if not success:
                    return False, f"Failed to install dependencies: {', '.join(missing_deps)}"
            else:
                return False, f"Missing dependencies: {', '.join(missing_deps)}"
        
        # Get platform-specific configuration
        platform_config = self.config_manager.get_platform_config(tool_config)
        if not platform_config:
            return False, f"No installation instructions for {tool_name} on this platform"
        
        # Run installation
        install_cmd = platform_config.get("install", "")
        if not install_cmd:
            return False, f"No install command defined for {tool_name}"
        
        # Create installation directory if needed
        install_path = self.config_manager.install_path / tool_name
        if not create_directory(install_path):
            return False, f"Failed to create installation directory: {install_path}"
        
        # Set environment variables if needed
        env_vars = platform_config.get("environment", {})
        original_env = os.environ.copy()
        for key, value in env_vars.items():
            os.environ[key] = value
        
        # Execute installation command
        logger.info(f"Installing {tool_name} with command: {install_cmd}")
        result = run_command(install_cmd)
        
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
        
        if result is None:
            return False, f"Installation of {tool_name} failed"
        
        # Add to PATH if configured
        if platform_config.get("add_to_path", False):
            add_to_path(install_path / "bin")
        
        # Set environment variables in user config
        self._save_environment_variables(tool_name, env_vars)
        
        return True, f"Successfully installed {tool_name}"
    
    def is_tool_installed(self, tool_name: str, tool_config: Dict[str, Any] = None) -> bool:
        """
        Check if a tool is installed
        
        Args:
            tool_name: Name of the tool to check
            tool_config: Tool configuration (optional)
        
        Returns:
            Boolean indicating if the tool is installed
        """
        if tool_config is None:
            tool_config = self.config_manager.get_tool_config(tool_name)
        
        if not tool_config:
            return False
        
        platform_config = self.config_manager.get_platform_config(tool_config)

        # Check using version command
        # Prioritize platform-specific version check, then fall back to the general one.
        version_cmd = platform_config.get("version_check", tool_config.get("version_check", ""))

        if version_cmd:
            result = run_command(version_cmd, capture_output=True, check=False, log_errors=False)
            if result and result.returncode == 0:
                return True
        
        # Check if executable exists in installation directory
        install_path = self.config_manager.install_path / tool_name
        exec_name = tool_config.get("executable", tool_name)
        
        if platform.system().lower() == "windows":
            exec_name += ".exe"
        
        exec_path = install_path / "bin" / exec_name
        if exec_path.exists():
            return True
        
        # Check if executable is in PATH
        from utils import is_tool_available
        if is_tool_available(exec_name):
            return True
        
        return False
    
    def prompt_install_dependencies(self, dependencies: List[str]) -> bool:
        """
        Prompt user to install missing dependencies
        
        Args:
            dependencies: List of missing dependencies
        
        Returns:
            Boolean indicating if user wants to install dependencies
        """
        try:
            from ui import prompt_yes_no
            message = f"The following dependencies are missing: {', '.join(dependencies)}. Do you want to install them?"
            return prompt_yes_no(message)
        except (ImportError, Exception) as e:
            # If UI is not available or another error occurs, log it and assume no.
            logger.error(f"Could not prompt user for dependency installation: {e}")
            return False
    
    def _save_environment_variables(self, tool_name: str, env_vars: Dict[str, str]):
        """
        Save environment variables to user config
        
        Args:
            tool_name: Name of the tool
            env_vars: Environment variables to save
        """
        if "environment" not in self.config_manager.user_config:
            self.config_manager.user_config["environment"] = {}
        
        if tool_name not in self.config_manager.user_config["environment"]:
            self.config_manager.user_config["environment"][tool_name] = {}
        
        self.config_manager.user_config["environment"][tool_name].update(env_vars)
        self.config_manager.save_user_config()