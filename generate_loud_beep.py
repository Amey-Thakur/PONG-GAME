import wave
import math
import struct
import os

def generate_loud_beep(filename, duration_ms=100, freq=880, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000.0)
    data = []
    
    # Square wave generation (Max Amplitude)
    for i in range(num_samples):
        t = float(i) / sample_rate
        # Square wave: +Max if sin > 0 else -Max
        if math.sin(2.0 * math.pi * freq * t) > 0:
            sample = 32767 # Max 16-bit signed integer
        else:
            sample = -32768 # Min 16-bit signed integer
            
        data.append(struct.pack('<h', sample))
        
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Writing WAV format but naming it .ogg as requested
    # Browsers often 'sniff' the content (RIFF header) and play it anyway.
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 16 bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(data))
    
    print(f"Generated LOUD beep at {filename}")

if __name__ == "__main__":
    # Generate: Source Code/sound/countdown.ogg (Actually WAV content)
    generate_loud_beep("Source Code/sound/countdown.ogg", duration_ms=150, freq=1000)
