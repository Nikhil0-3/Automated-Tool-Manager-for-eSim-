"""
Configuration handling for the eSim Tool Manager
"""

import json
from pathlib import Path
from typing import Dict, Any

from constants import CONFIG_FILE, USER_CONFIG_FILE, DEFAULT_PATHS, SYSTEM
from logger import logger

class ConfigManager:
    def __init__(self):
        self.tools_config = self.load_config(CONFIG_FILE)
        self.user_config = self.load_config(USER_CONFIG_FILE)
        self.install_path = self.get_install_path()
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Args:
            config_file: Path to the configuration file
        
        Returns:
            Dictionary with configuration data
        """
        config_path = Path(config_file)
        if not config_path.exists():
            logger.warning(f"Configuration file {config_file} not found")
            return {}
            
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file {config_file}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error reading configuration file {config_file}: {e}")
            return {}
    
    def save_user_config(self):
        """
        Save user configuration to file
        """
        try:
            with open(USER_CONFIG_FILE, 'w') as f:
                json.dump(self.user_config, f, indent=4)
            logger.info("User configuration saved")
            return True
        except Exception as e:
            logger.error(f"Error saving user configuration: {e}")
            return False
    
    def get_install_path(self) -> Path:
        """
        Get the installation path for tools
        
        Returns:
            Path object for installation directory
        """
        # Check user config first
        if "install_path" in self.user_config:
            return Path(self.user_config["install_path"])
        
        # Fall back to default based on OS
        return DEFAULT_PATHS[SYSTEM]
    
    def set_install_path(self, path: str):
        """
        Set the installation path for tools
        
        Args:
            path: New installation path
        """
        path_obj = Path(path)
        self.user_config["install_path"] = str(path_obj)
        self.install_path = path_obj
        self.save_user_config()
        logger.info(f"Installation path set to {path}")
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific tool
        
        Args:
            tool_name: Name of the tool
        
        Returns:
            Dictionary with tool configuration
        """
        return self.tools_config.get("tools", {}).get(tool_name, {})
    
    def get_all_tools(self) -> Dict[str, Any]:
        """
        Get configuration for all tools
        
        Returns:
            Dictionary with all tools configuration
        """
        return self.tools_config.get("tools", {})
    
    def get_platform_config(self, tool_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get platform-specific configuration for a tool
        
        Args:
            tool_config: Tool configuration dictionary
        
        Returns:
            Platform-specific configuration
        """
        from constants import SYSTEM
        from utils import get_linux_distro
        
        if SYSTEM in tool_config:
            # This handles 'windows' and 'darwin' directly
            return tool_config.get(SYSTEM, {})
        elif SYSTEM == "linux":
            distro = get_linux_distro()
            linux_config = tool_config.get("linux", {})
            # Return distro-specific config, or the general linux config if available
            return linux_config.get(distro, linux_config)
        
        return {}