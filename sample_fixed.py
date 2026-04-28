import soundfile as sf
from scipy.signal import resample

input_file = "sample.wav"
output_file = "sample_fixed.wav"

# Read original
data, sr = sf.read(input_file)

# Convert stereo → mono (if needed)
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Resample to 16000 Hz if needed
target_sr = 16000
if sr != target_sr:
    num_samples = int(len(data) * target_sr / sr)
    data = resample(data, num_samples)

# Save as 16-bit PCM WAV
sf.write(output_file, data, target_sr, subtype="PCM_16")

print("Converted successfully → sample_fixed.wav")
