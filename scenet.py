import json

def create_scene_timings(wordtiming_file_path, scenes_file_path, output_file_path):
    # Load JSON files
    with open(wordtiming_file_path, 'r') as wordtiming_file:
        wordtiming_data = json.load(wordtiming_file)

    with open(scenes_file_path, 'r') as scenes_file:
        scenes_data = json.load(scenes_file)

    # Create a list of scenes with start and end times
    scenes_timing = {}
    current_index = 0

    for scene_key, scene_text in scenes_data.items():
        # Split the scene text into words
        scene_words = scene_text.split()
        word_count = len(scene_words)

        # Get the corresponding words from wordtiming_data
        scene_word_timings = wordtiming_data[current_index:current_index + word_count]

        # Calculate start and end times for the scene
        if scene_word_timings:
            scene_start_time = scene_word_timings[0]["start_time"]
            scene_end_time = scene_word_timings[-1]["end_time"]

            scenes_timing[scene_key] = {
                "start_time": scene_start_time,
                "end_time": scene_end_time
            }
        else:
            print(f"Error: Unable to determine timings for scene '{scene_key}'.")

        # Update the current index
        current_index += word_count

    # Save the new JSON file with scene start and end times
    with open(output_file_path, 'w') as output_file:
        json.dump(scenes_timing, output_file, indent=4)

if __name__ == "__main__":
    wordtiming_file_path = "wordtiming.json"
    scenes_file_path = "scenes.json"
    output_file_path = "scenes_timing.json"

    create_scene_timings(wordtiming_file_path, scenes_file_path, output_file_path)