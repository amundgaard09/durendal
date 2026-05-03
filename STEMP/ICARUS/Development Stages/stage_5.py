"""ICARUS Autonomous Tactical Assistant - STAGE V - TTS Testing"""

from piper import PiperVoice
import wave

ONNX = "C:/Users/Administrator/.vscode/AmundWorks/amundworks/STEMP/ICARUS/Dependencies/en_US-arctic-medium.onnx"

voice = PiperVoice.load(ONNX) 

with wave.open("test.wav", "wb") as wav_file: 
    voice.synthesize_wav("Icarus online. All systems nominal", wav_file)


print("Done - play icarus_online.wav")
