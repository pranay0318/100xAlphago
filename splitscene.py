import json

def split_text_into_scenes(filename, num_scenes=15, output_file="scenes.json"):
    with open(filename, "r", encoding="utf-8") as file:
        words = file.read().split()
    
    total_words = len(words)
    chunk_size = total_words // num_scenes
    remainder = total_words % num_scenes
    
    scenes = {}
    start = 0
    for i in range(num_scenes):
        end = start + chunk_size + (1 if i < remainder else 0)
        scenes[f"scene{i + 1}"] = " ".join(words[start:end])
        start = end
    
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(scenes, json_file, indent=4, ensure_ascii=False)
    
    print(f"Scenes saved to {output_file}")

# Run the function
split_text_into_scenes("script.txt")
