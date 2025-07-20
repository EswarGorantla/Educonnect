import whisper
import sys

# Get audio file path from command-line argument
audio_path = sys.argv[1]

# Load Whisper model
model = whisper.load_model("base")

# Transcribe audio
result = model.transcribe(audio_path)

# Print segments with timestamps
for segment in result['segments']:
    print(f"[{segment['start']}s - {segment['end']}s]: {segment['text']}")

# Optional: Save full text
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(result['text'])
