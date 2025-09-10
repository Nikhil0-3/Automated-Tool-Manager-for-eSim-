"""
User interface components for the eSim Tool Manager, such as prompts.
"""

from logger import logger

def prompt_yes_no(message: str) -> bool:
    """
    Display a yes/no prompt to the user in the command line.

    Args:
        message: The question to ask the user.

    Returns:
        Boolean indicating the user's choice.
    """
    reply = str(input(f"{message} (y/n): ")).lower().strip()
    return reply[:1] == 'y'