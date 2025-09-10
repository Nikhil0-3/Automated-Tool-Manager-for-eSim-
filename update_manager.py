"""
Update checking and handling for the eSim Tool Manager
"""

from typing import Dict, List, Tuple, Any

from config_manager import ConfigManager
from install_manager import InstallManager
from utils import run_command
from logger import logger

class UpdateManager:
    def __init__(self, config_manager: ConfigManager, install_manager: InstallManager):
        self.config_manager = config_manager
        self.install_manager = install_manager
    
    def check_updates(self) -> Dict[str, str]:
        """
        Check for available updates for all installed tools
        
        Returns:
            Dictionary with tool names and update status
        """
        updates = {}
        tools = self.config_manager.get_all_tools()
        
        for tool_name, tool_config in tools.items():
            if self.install_manager.is_tool_installed(tool_name, tool_config):
                status = self._check_tool_update(tool_name, tool_config)
                if status:
                    updates[tool_name] = status
        
        return updates
    
    def update_tool(self, tool_name: str) -> Tuple[bool, str]:
        """
        Update a tool
        
        Args:
            tool_name: Name of the tool to update
        
        Returns:
            Tuple of (success status, message)
        """
        # Get tool configuration
        tool_config = self.config_manager.get_tool_config(tool_name)
        if not tool_config:
            return False, f"Tool {tool_name} not found in configuration"
        
        # Check if tool is installed
        if not self.install_manager.is_tool_installed(tool_name, tool_config):
            return False, f"Tool {tool_name} is not installed"
        
        # Get platform-specific configuration
        platform_config = self.config_manager.get_platform_config(tool_config)
        if not platform_config:
            return False, f"No update instructions for {tool_name} on this platform"
        
        # Run update
        update_cmd = platform_config.get("update", "")
        if not update_cmd:
            return False, f"No update command defined for {tool_name}"
        
        logger.info(f"Updating {tool_name} with command: {update_cmd}")
        result = run_command(update_cmd)
        
        if result is None:
            return False, f"Update of {tool_name} failed"
        
        return True, f"Successfully updated {tool_name}"
    
    def update_all_tools(self) -> Dict[str, Tuple[bool, str]]:
        """
        Update all installed tools
        
        Returns:
            Dictionary with tool names and update results
        """
        results = {}
        tools = self.config_manager.get_all_tools()
        
        for tool_name, tool_config in tools.items():
            if self.install_manager.is_tool_installed(tool_name, tool_config):
                success, message = self.update_tool(tool_name)
                results[tool_name] = (success, message)
        
        return results
    
    def _check_tool_update(self, tool_name: str, tool_config: Dict[str, Any]) -> str:
        """
        Check for updates for a specific tool
        
        Args:
            tool_name: Name of the tool to check
            tool_config: Tool configuration
        
        Returns:
            Update status message or empty string if no update available
        """
        # Get platform-specific configuration
        platform_config = self.config_manager.get_platform_config(tool_config)
        if not platform_config:
            return "Could not determine update status for this platform"
        
        # Check using update check command if available
        update_check_cmd = platform_config.get("update_check", "")
        if update_check_cmd:
            result = run_command(update_check_cmd, capture_output=True, check=False)
            if result and result.stdout and tool_name in result.stdout:
                return "Update available"
        
        return "Up to date"
        