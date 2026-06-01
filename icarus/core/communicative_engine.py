"""
The `ICARUS` Complex Speech Engine

This file contains dependencies for ICARUS linked to speaking and listening.

---

The ICARUS Complex is an AmundWorks project. More information can be found at the [AmundWorks GitHub](https://github.com/amundgaard09/amundworks/)
"""

import io, pydub, struct, pyaudio, pvporcupine, speech_recognition
import pydub.playback as playback
import pydub.utils as pd_utils

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from durapy.src.unipy.uniCLI import console_print

# ICARUS Wake Word Detector Model path
_I_WWD_MODEL = r""

recognizer = speech_recognition.Recognizer()
elevenlabs = ElevenLabs(api_key="sk_7f76849a92b748cdcb851cfdf95f86ed75faddde8d306afd")

pydub.AudioSegment.converter = pd_utils.which("C:/ffmpeg/bin/ffmpeg.exe")

def __play_audio(audio_bytes: bytes) -> None:
    """
    Play the given audio bytes
    """
    audio_buffer = io.BytesIO(audio_bytes)
    audio_segment = pydub.AudioSegment.from_file(audio_buffer)
    playback.play(audio_segment)

def _speak(text: str) -> None:
    """
    Speak the given text through `ElevenLabs` TTS.
    """
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
    __play_audio(audio_stream.read())
    console_print("ICARUS", "blue", text)
    

def _initializer() -> bool:
    """
    Initialize ICARUS and listen for wake/hot word (`ICARUS`)
    """
    porcupine = pvporcupine.create(
        access_key="ithh0auyq3aCHZb8ofPTmnOGPv+B5ZXzkP4lEUWBnR1i/h1T2dol9g==",
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
    
    console_print("ICARUS", "blue", "Listening for Icarus ...")
    
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                console_print("ICARUS", "blue", "Activating Icarus I ...", "green")
                return True
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def listen_for_command(repeat: bool = False) -> str:
    with speech_recognition.Microphone() as src:
        if not repeat:
            console_print("ICARUS", "blue", "Listening ...")
            _speak("At your service.")
        sound = recognizer.listen(src)

        try:             ### TODO switch from whisper to non depecrated recognizer
            cmd = str(recognizer.recognize_whisper(sound, language="en-US"))
            return cmd.lower()
        
        except speech_recognition.UnknownValueError:
            _speak("I didn't understand that.")
            return listen_for_command(True)
        
        except speech_recognition.RequestError:
            _speak("I am unavailable at this time.")
            return ""

# TODO Only for testing, remove once finished and shipped
if __name__ == "__main__":
    if _initializer():
        listen_for_command()