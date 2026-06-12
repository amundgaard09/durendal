
from durapy import uniCLI

from core.engines.intent_engine import (
    initialize as intent_engine_init
)

from core.engines.execution_engine import (
    initialize as exec_engine_init, 
    respond
)

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
            response = respond(user_input)
            speak(response)

exec_engine_init()
intent_engine_init()
comms_engine_init()
main()
