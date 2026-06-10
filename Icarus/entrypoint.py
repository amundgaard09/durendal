
from durapy import uniCLI
from core.mcp.skill_loaders import get_py_skill_and_triggers
from core.engines.execution_engine import process
from core.engines.communicative_engine import (
    initialize as comms_engine_init, 
    listen, speak
)

def main() -> None:
    """The main speech kernel for the Icarus Complex"""
    uniCLI.console_print("ICARUS", "blue", "Listening...", "green")
    while True:
        user_input = listen()
        
        if "goodbye" in user_input:
            speak("Goodbye, Simon")
            exit(1)
            
        else:
            response = process(user_input)
            speak(response)
    
comms_engine_init()
main()