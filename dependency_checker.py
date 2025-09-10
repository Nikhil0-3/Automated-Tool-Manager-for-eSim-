"""
Dependency checking for the eSim Tool Manager
"""
import distro

import shutil
from typing import Dict, List, Tuple, Any

from constants import SYSTEM, PACKAGE_MANAGERS
from utils import is_tool_available, run_command
from logger import logger

def get_linux_distro() -> str:
    """Get Linux distribution ID using the 'distro' library."""
    if SYSTEM != "linux":
        return ""
    return distro.id()

class DependencyChecker:
    """Checks for and manages tool and system dependencies."""

    def __init__(self):
        self.system_dependencies = self.get_system_dependencies()
        self.available_package_manager = self.get_package_manager()
    
    def get_system_dependencies(self) -> List[str]:
        """
        Get system-level dependencies based on OS
        """
        if SYSTEM == "linux":
            return ["curl", "wget", "tar", "gzip"]
        elif SYSTEM == "windows":
            return ["powershell"]
        elif SYSTEM == "darwin":
            return ["curl", "wget", "tar", "gzip"]
        return []
    
    def get_package_manager(self) -> str:
        """
        Get the available package manager for the system
        """
        if SYSTEM == "windows":
            if is_tool_available("choco"):
                return "choco"
        elif SYSTEM == "darwin":
            if is_tool_available("brew"):
                return "brew"
        elif SYSTEM == "linux":
            distro = get_linux_distro()
            if distro in PACKAGE_MANAGERS["linux"]:
                pm = PACKAGE_MANAGERS["linux"][distro]
                if is_tool_available(pm):
                    return pm
        
        return ""
    
    def check_system_dependencies(self) -> Tuple[bool, List[str]]:
        """
        Check if system dependencies are available
        """
        missing = []
        for dep in self.system_dependencies:
            if not is_tool_available(dep):
                missing.append(dep)
        
        if missing:
            logger.warning(f"Missing system dependencies: {', '.join(missing)}")
            return False, missing
        
        logger.info("All system dependencies are available")
        return True, []
    
    def check_tool_dependencies(self, tool_config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check dependencies for a specific tool
        """
        dependencies = tool_config.get("dependencies", [])
        missing = []
        
        for dep in dependencies:
            if not is_tool_available(dep):
                missing.append(dep)
        
        if missing:
            logger.warning(f"Missing dependencies for tool: {', '.join(missing)}")
            return False, missing
        
        logger.info("All tool dependencies are available")
        return True, []
    
    def install_system_dependencies(self, dependencies: List[str]) -> bool:
        """
        Install system dependencies using the available package manager
        """
        if not self.available_package_manager:
            logger.error("No package manager available to install dependencies")
            return False
        
        if SYSTEM == "windows" and self.available_package_manager == "choco":
            command = f"choco install {' '.join(dependencies)} -y"
        elif SYSTEM == "darwin" and self.available_package_manager == "brew":
            command = f"brew install {' '.join(dependencies)}"
        elif SYSTEM == "linux" and self.available_package_manager:
            # Generic command for apt, dnf, yum etc.
            command = f"sudo {self.available_package_manager} install -y {' '.join(dependencies)}"
        else:
            logger.error(f"Unsupported package manager: {self.available_package_manager}")
            return False
        
        logger.info(f"Installing dependencies: {', '.join(dependencies)}")
        result = run_command(command)
        return result is not None