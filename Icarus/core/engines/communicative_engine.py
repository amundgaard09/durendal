
import io, os, json, queue, dotenv, sounddevice
import pydub, pydub.playback as pd_playback

from skills.timeskill import main as time_skill
from vosk import Model, KaldiRecognizer
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from durapy import uniCLI

_SPEECH_MODEL_PATH = r"C:\Users\Administrator\.vscode\durendal\Icarus\core\models\vosk-model-small-en-us-0.15"
dotenv.load_dotenv(r"C:\\Users\\Administrator\\.vscode\\durendal\\.env", verbose=True, encoding="utf-8")

_queue = queue.Queue()
model = Model(_SPEECH_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
elevenlabs = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))

def console_print(*args):
    return uniCLI.console_print(*args)

def callback(indata, frames, time, status):
    _queue.put(bytes(indata))

def play_audio(audio_bytes: bytes) -> None:
    """Play the given audio bytes."""
    audio_buffer = io.BytesIO(audio_bytes)
    audio_segment = pydub.AudioSegment.from_file(audio_buffer)
    pd_playback.play(audio_segment)

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
    play_audio(audio_stream.read())
    uniCLI.console_print("ICARUS", "blue", text)
    
def listen_for_command() -> str:
    with sounddevice.RawInputStream(
        samplerate=16000, 
        blocksize=8000, 
        dtype="int16", 
        channels=1, 
        callback=callback
        ):
    
        while True:
            data = _queue.get()

            if recognizer.AcceptWaveform(data):
                result: dict = json.loads(recognizer.Result())
                console_print("USER", "green", result.get("text").capitalize())
                return result.get("text", "")

def initialize() -> None:
    """Placeholder for future init logic for the Comms Engine."""
    console_print("ICARUS", "blue", "Initializing Icarus Communicative Engine...", "white")

def process(text: str) -> str:
    if "hello" in text:
        return "Hello, Simon"
    elif "you" in text:
        return "I am Icarus. I am a natural language AI agent built by Simon Stordal Amundgård for multi-diciplinary engineering tasks."
    elif "exit" in text or "goodbye" in text:
        return "Goodbye, Simon"
    elif "time" in text:
        return time_skill()
    else:
        return "I didn't understand that."
    
def kernel() -> str:
    """The main speech kernel for the Icarus Communicative Engine."""
    console_print("ICARUS", "blue", "Listening...", "green")
    while True:
        user_input = listen_for_command()
        if not user_input:
            speak("I didn't understand that.")
        
        response = process(user_input)
        
        if response == "Goodbye, Simon":
            speak(response)
            exit(1)
        else:
            speak(response)

initialize()
kernel()
            
            