import requests
import json
import base64
import os

VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Rachel
from dotenv import load_dotenv
load_dotenv()
YOUR_XI_API_KEY = os.getenv("XI_API_KEY")

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"

headers = {
  "Content-Type": "application/json",
  "xi-api-key": YOUR_XI_API_KEY
}

# Read the text from the input file
with open("script.txt", "r", encoding="utf-8") as file:
    text = file.read()

data = {
  "text": text,
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}

response = requests.post(
    url,
    json=data,
    headers=headers,
)

if response.status_code != 200:
  print(f"Error encountered, status: {response.status_code}, "
        f"content: {response.text}")
  quit()

# convert the response which contains bytes into a JSON string from utf-8 encoding
json_string = response.content.decode("utf-8")

# parse the JSON string and load the data as a dictionary
response_dict = json.loads(json_string)

# the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string,
# we need to decode it into bytes in order to save the audio as a file
audio_bytes = base64.b64decode(response_dict["audio_base64"])

# Save the audio to 'full_audio.mp3'
with open('full_audio.mp3', 'wb') as f:
  f.write(audio_bytes)

# the 'alignment' entry contains the mapping between input characters and their timestamps
with open('alignment.json', 'w') as alignment_file:
    json.dump(response_dict['alignment'], alignment_file, ensure_ascii=False, indent=2)

print("Alignment saved to 'alignment.json'")