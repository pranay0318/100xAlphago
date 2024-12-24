import os
import replicate
import json
import requests
from dotenv import load_dotenv

# Load the API token
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.makedirs("generated_images", exist_ok=True)

# Load image prompts from JSON
with open("image_prompts.json", "r") as file:
    prompts = json.load(file)


style="2d Drawing style, Colorful, Pastel Feel, without morphing, perfect anatomy"

# Generate images for each scene
for scene, prompt in prompts.items():
    styled_prompt = f"{style}, {prompt}"
    input_params = {
        "prompt": styled_prompt,
        "aspect_ratio": "9:16",
        "output_format": "png"
    }

    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input=input_params
    )

    for index, url in enumerate(output):
        response = requests.get(url)
        if response.status_code == 200:
            output_path = os.path.join("generated_images", f"{scene}_{index}.png")
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Image for {scene} saved as {output_path}.")
        else:
            print(f"Failed to download image for {scene}: {url}")
