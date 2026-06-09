
from durapy import uniCLI
from core.mcp.skill_loaders import get_py_skill
from core.engines.communicative_engine import (
    initialize as comms_engine_init, 
    listen, speak, process
)

def main() -> None:
    """The main speech kernel for the Icarus Complex"""
    uniCLI.console_print("ICARUS", "blue", "Listening...", "green")
    while True:
        user_input = listen()
        response = process(user_input)
        
        if response == "Goodbye, Simon":
            speak(response)
            exit(1)
        else:
            speak(response)
    
comms_engine_init()
main()