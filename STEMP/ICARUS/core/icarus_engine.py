
import struct, pyaudio, pvporcupine, speech_recognition as Speech

from io import BytesIO
from pydub import AudioSegment
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub.playback import play
from pydub.utils import which

recognizer = Speech.Recognizer()

# Sett API-nøkkel (kan også settes i miljøvariabler)
elevenlabs = ElevenLabs(
    api_key="sk_7f76849a92b748cdcb851cfdf95f86ed75faddde8d306afd"
)

# Sett sti til ffmpeg-binær (tilpass til din installasjon)
AudioSegment.converter = which("C:/ffmpeg/bin/ffmpeg.exe")

def play_audio(audio_bytes: bytes):
    audio_buffer = BytesIO(audio_bytes)
    audio_segment = AudioSegment.from_file(audio_buffer)
    play(audio_segment)

def speak(text: str):
    # Stream lyd som mp3 i chunks, samle i BytesIO
    response = elevenlabs.text_to_speech.stream(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Eksempelstemme "Adam"
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
            speed=1.0,
        ),
    )
    audio_stream = BytesIO()
    for chunk in response:
        if chunk:
            audio_stream.write(chunk)

    audio_stream.seek(0)
    play_audio(audio_stream.read())  # Spill av lyden

def initializer() -> bool:
    porcupine = pvporcupine.create(
        access_key="ithh0auyq3aCHZb8ofPTmnOGPv+B5ZXzkP4lEUWBnR1i/h1T2dol9g==",
        keyword_paths=[r"C:\\Users\\MAU\\.vscode\\amundworks\\python_\\icarus_v1\\Icarus_en_windows_v3_0_0.ppn"]
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Listening for 'Icarus'...")
    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:
                print("Activating Icarus I")
                return True
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

def cmdlisten(repeat: bool) -> str:
    with Speech.Microphone() as src:
        if not repeat:
            print("Listening...")
            speak("At your service.")
        sound = recognizer.listen(src)

        try:
            cmd: str = recognizer.recognize_google(sound, language="en-US")
            print(f"[ICARUS] CMD: {cmd}")
            return cmd.lower()
        except Speech.UnknownValueError:
            speak("I didn't understand that.")
            return cmdlisten(True)
        except Speech.RequestError:
            speak("I am unavailable at this time.")
            return ""

def cmdexe(kommando: str):
    pass

if __name__ == "__main__":
    if initializer():
        cmdlisten(False)