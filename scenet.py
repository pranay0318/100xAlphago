import json

# Load word timing, scenes, and script files
with open("wordtiming.json", "r") as wt_file:
    word_timings = json.load(wt_file)

with open("scenes.json", "r") as sc_file:
    scenes = json.load(sc_file)

with open("script.txt", "r") as script_file:
    script_text = script_file.read()

def get_scene_timing(scene_text, word_timings):
    words = scene_text.split()
    start_time = None
    end_time = None

    for timing in word_timings:
        if start_time is None and timing["word"].lower() == words[0].lower():
            start_time = timing["start_time"]

        if timing["word"].lower() == words[-1].lower():
            end_time = timing["end_time"]

        if start_time and end_time:
            break

    return start_time, end_time

scene_timing = {}

for scene_name, scene_fragment in scenes.items():
    # Match scene fragment to the script
    if scene_fragment in script_text:
        start, end = get_scene_timing(scene_fragment, word_timings)
        scene_timing[scene_name] = {"start_time": start, "end_time": end}
    else:
        scene_timing[scene_name] = {"start_time": None, "end_time": None}  # Handle unmatched scenes

# Save the scene timing JSON file
with open("scenetiming.json", "w") as st_file:
    json.dump(scene_timing, st_file, indent=4)

print("Scenetiming.json has been created successfully.")
