
import io, os, json, queue, dotenv, sounddevice
import pydub, pydub.playback as pd_playback

from core.utilities.decorators import logger
from vosk import Model, KaldiRecognizer
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from durapy import uniCLI
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_SPEECH_MODEL_PATH = ROOT / "core" / "models" / "vosk-model-small-en-us-0.15"
dotenv.load_dotenv(Path(__file__).resolve().parents[3] / ".env", verbose=True, encoding="utf-8")

_queue = queue.Queue()
model = Model(str(_SPEECH_MODEL_PATH))
recognizer = KaldiRecognizer(model, 16000)
elevenlabs = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

def _callback(indata, frames, time, status):
    _queue.put(bytes(indata))

def _play_audio(audio_bytes: bytes) -> None:
    """Play the given audio bytes."""
    audio_buffer = io.BytesIO(audio_bytes)
    audio_segment = pydub.AudioSegment.from_file(audio_buffer)
    pd_playback.play(audio_segment)

@logger
def speak(text: str) -> None:
    """Speak the given text through `ElevenLabs` TTS. Also logs the text to the terminal"""
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
            speed = 0.95,
        )
    )
    
    audio_stream = io.BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    audio_stream.seek(0)
    _play_audio(audio_stream.read())
    uniCLI.console_print("ICARUS", "blue", text)

@logger   
def listen() -> str:
    with sounddevice.RawInputStream(
        samplerate=16000, 
        blocksize=8000, 
        dtype="int16", 
        channels=1, 
        callback=_callback
        ):
    
        while True:
            data = _queue.get()

            if recognizer.AcceptWaveform(data):
                result: dict = json.loads(recognizer.Result())
                uniCLI.console_print("USER", "green", result.get("text").capitalize())
                return result.get("text", "")

@logger
def initialize() -> None:
    """Placeholder for future init logic for the Comms Engine."""
    uniCLI.console_print("ICARUS", "blue", "Initializing Icarus Communicative Engine...", "white")

