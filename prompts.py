import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
style="2d Drawing style, Colorful, Pastel Feel, without morphing, perfect anatomy"

def generate_prompt(scene, context):
    """Generates a short and accurate image prompt based on the scene and context."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an AI assistant creating concise and vivid image prompts of 200 characters with the style of {style} for each scene based on the story context. The prompt should be highlighting dynamic elements in the scene, And should refer to the action occuring in the specific scene."},
            {"role": "user", "content": f"Context: {context}\nScene: {scene}\nCreate a vivid image prompt for this scene."}
        ]
    )
    return response.choices[0].message.content

# Load the JSON file with the scenes
with open('scenes.json', 'r', encoding="utf-8") as file:
    scenes = json.load(file)

# Read the context from the script file
with open('script.txt', 'r', encoding="utf-8") as file:
    context = file.read().strip()

# Generate prompts for each scene
prompts = {}
for scene_id, scene_text in scenes.items():
    prompt = generate_prompt(scene_text, context)
    prompts[scene_id] = prompt

# Save the prompts to a new JSON file
output_file = 'image_prompts.json'
with open(output_file, 'w', encoding="utf-8") as file:
    json.dump(prompts, file, indent=4)

print(f"Image prompts saved to {output_file}")
