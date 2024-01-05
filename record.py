import sounddevice as sd
from scipy.io.wavfile import write

def record_voice(duration=5, sample_rate=44100):
    print("Recording...")

    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()

    print("Recording done.")

    return audio_data, sample_rate

def save_audio(audio_data, sample_rate, filename="granttest.wav"):
    # Save audio to a file using scipy
    write(filename, sample_rate, audio_data)
    print(f"Audio saved to {filename}")

if __name__ == "__main__":
    duration = 5  # Specify the recording duration in seconds

    # Record audio
    audio_data, sample_rate = record_voice(duration)

    # Save audio to a file
    save_audio(audio_data, sample_rate)

