"""
Main entry point for the eSim Automated Tool Manager CLI.
"""

import argparse
from logger import logger
from config_manager import ConfigManager
from install_manager import InstallManager
from update_manager import UpdateManager

def main():
    """Main function to handle command-line arguments."""
    # --- Setup ---
    config_manager = ConfigManager()
    install_manager = InstallManager(config_manager)
    update_manager = UpdateManager(config_manager, install_manager)

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description="eSim Automated Tool Manager. Manages installation, updates, and configuration of external tools."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # 'install' command
    parser_install = subparsers.add_parser("install", help="Install a tool.")
    parser_install.add_argument("tool_name", help="The name of the tool to install (e.g., ngspice, kicad).")

    # 'update' command
    parser_update = subparsers.add_parser("update", help="Update a tool or check for updates.")
    parser_update.add_argument(
        "tool_name",
        nargs="?",  # Make tool_name optional
        default=None,
        help="The name of the tool to update. If not provided, checks all installed tools for updates."
    )
    parser_update.add_argument(
        "--all",
        action="store_true",
        help="Update all installed tools."
    )

    # 'list' command
    parser_list = subparsers.add_parser("list", help="List all available and installed tools.")

    # 'uninstall' command
    parser_uninstall = subparsers.add_parser("uninstall", help="Uninstall a tool.")
    parser_uninstall.add_argument("tool_name", help="The name of the tool to uninstall.")

    # 'set-path' command
    parser_path = subparsers.add_parser("set-path", help="Set the base installation directory for tools.")
    parser_path.add_argument("path", help="The new absolute path for tool installations.")

    args = parser.parse_args()

    # --- Command Execution ---
    if args.command == "install":
        logger.info(f"Attempting to install '{args.tool_name}'...")
        success, message = install_manager.install_tool(args.tool_name)
        if success:
            logger.info(message)
        else:
            logger.error(message)

    elif args.command == "update":
        if args.all:
            logger.info("Updating all installed tools...")
            results = update_manager.update_all_tools()
            for tool, (success, message) in results.items():
                if success:
                    logger.info(f"'{tool}': {message}")
                else:
                    logger.error(f"'{tool}': {message}")
        elif args.tool_name:
            logger.info(f"Attempting to update '{args.tool_name}'...")
            success, message = update_manager.update_tool(args.tool_name)
            if success:
                logger.info(message)
            else:
                logger.error(message)
        else:
            logger.info("Checking for available updates...")
            updates = update_manager.check_updates()
            if not updates:
                logger.info("All tools are up to date.")
            else:
                for tool, status in updates.items():
                    logger.info(f"- {tool}: {status}")

    elif args.command == "list":
        logger.info("Available tools:")
        all_tools = config_manager.get_all_tools()
        for tool_name, config in all_tools.items():
            installed_status = " (installed)" if install_manager.is_tool_installed(tool_name, config) else ""
            description = config.get('description', 'No description')
            logger.info(f"- {tool_name}{installed_status}: {description}")

    elif args.command == "uninstall":
        logger.info(f"Attempting to uninstall '{args.tool_name}'...")
        success, message = install_manager.uninstall_tool(args.tool_name)
        if success:
            logger.info(message)
        else:
            logger.error(message)

    elif args.command == "set-path":
        logger.info(f"Setting new installation path to '{args.path}'...")
        config_manager.set_install_path(args.path)

if __name__ == "__main__":
    main()