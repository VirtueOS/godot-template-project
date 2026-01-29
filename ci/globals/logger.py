from datetime import datetime
from colorama import Fore, Style


class Logger:

    def __init__(self,
                 show_timestamp: bool = True,
                ):
        """
        Initialize the logger
        
        Args:
            name: Logger name
            show_timestamp: Show timestamp in log messages
            show_level: Show log level in messages
            log_to_file: Enable file logging
            log_file: Log file path
        """

        self.show_timestamp = show_timestamp


    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _format_message(self, msg:str, color:str, indent:int = 2) -> str:
        if self.show_timestamp:
            msg = self._get_timestamp() + " " + msg
        indent_str = " " * indent
        return f"{color}{indent_str}>>> {msg}{Style.RESET_ALL}"


    def print_error(self, msg: str, indent:int = 2):
        print(self._format_message(f"Error: {msg}", Fore.RED, indent))
    
    def print_warning(self, msg: str, indent:int = 2):
        print(self._format_message(f"Warning: {msg}", Fore.YELLOW, indent))
    
    def print_success(self, msg: str, indent:int = 2):
        print(self._format_message(f"{msg}", Fore.GREEN, indent))
    
    def print_log(self, msg: str, indent:int = 2):
        print(self._format_message(f"{msg}", Fore.WHITE, indent))
    
    def print_debug(self, msg: str, indent:int = 2):
        print(self._format_message(f"{msg}", Fore.MAGENTA, indent))

    def _example_print(self):
        self.print_error("Example Error")
        self.print_warning("Example Warning")
        self.print_success("Example Success")
        self.print_log("Example Log")
        self.print_debug("Example Debug")