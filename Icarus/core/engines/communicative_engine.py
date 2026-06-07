"""
The `ICARUS` Complex Speech Engine

This file contains dependencies for ICARUS linked to speaking and listening.

---

The ICARUS Complex is a Durendal project. More information can be found at the [Durendal GitHub](https://github.com/amundgaard09/durendal/)
"""

import io, os, pydub, dotenv, struct, pyaudio, pvporcupine, speech_recognition
import pydub.playback as playback
import pydub.utils as pd_utils

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from durapy import uniCLI

# ICARUS Wake Word Detector Model path
_I_WWD_MODEL = r""
_MODELS_PATH = r"C:\\Users\\Administrator\\.vscode\\durendal\\Icarus\\core\\models"

dotenv.load_dotenv(r"C:\\Users\\Administrator\\.vscode\\durendal\\.env", verbose=True, encoding="utf-8")

recognizer = speech_recognition.Recognizer()
elevenlabs = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API"))

pydub.AudioSegment.converter = pd_utils.which("C:/ffmpeg/bin/ffmpeg.exe")

def play_audio(audio_bytes: bytes) -> None:
    """Play the given audio bytes."""
    audio_buffer = io.BytesIO(audio_bytes)
    audio_segment = pydub.AudioSegment.from_file(audio_buffer)
    playback.play(audio_segment)

def speak(text: str) -> None:
    """Speak the given text through `ElevenLabs` TTS."""
    response = elevenlabs.text_to_speech.stream(
        voice_id="pNInz6obpgDQGcFmaJgB",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings = VoiceSettings(
            stability = 0.0,
            similarity_boost = 1.0,
            style = 0.0,
            use_speaker_boost = True,
            speed = 1.0,
        )
    )
    
    audio_stream = io.BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    audio_stream.seek(0)
    play_audio(audio_stream.read())
    uniCLI.console_print("ICARUS", "blue", text)
    

def initializer() -> bool:
    """
    Initialize ICARUS and listen for wake/hot word (`ICARUS`)
    """
    
    uniCLI.console_print("ICARUS", "blue", "Initializing Icarus Commicative Engine...", "blue")
     
    porcupine = pvporcupine.create(
        access_key=os.environ.get("PICOVOICE_API"),
        keyword_paths=[_I_WWD_MODEL]
    )
    
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    
    uniCLI.console_print("ICARUS", "blue", "Icarus is up and running!", "green")
    uniCLI.console_print("ICARUS", "blue", "Listening for Icarus ...")
    
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0: # Wake word detected
                uniCLI.console_print("ICARUS", "blue", "Activating Icarus I ...", "green")
                return True
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def listen_for_command(repeat: bool = False) -> str:
    with speech_recognition.Microphone() as src:
        if not repeat:
            uniCLI.console_print("ICARUS", "blue", "Listening ...")
            speak("At your service.")
            
        sound = recognizer.listen(src)

        try:
            cmd = str(recognizer.recognize_tensorflow(sound, _MODELS_PATH + "\\conv_actions_frozen.pb", _MODELS_PATH + "\\conv_actions_labels.txt" ))
            return cmd.lower()
        
        except speech_recognition.UnknownValueError:
            speak("I didn't understand that.")
            uniCLI.console_print("ICARUS", "blue", "speech_recognition.UnknownValueError", "red")
            return listen_for_command(repeat=True)
        
        except speech_recognition.RequestError:
            speak("I am unavailable at this time.")
            uniCLI.console_print("ICARUS", "blue", "speech_recognition.RequestError", "red")
            return ""

# TODO Only for testing, remove once finished and shipped
if __name__ == "__main__":
    if initializer():
        listen_for_command()