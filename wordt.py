import json

# File paths
alignment_file = 'alignment.json'
script_file = 'script.txt'
output_file = 'wordtiming.json'

# Load alignment JSON
with open(alignment_file, 'r') as f:
    alignment = json.load(f)

# Load script text
with open(script_file, 'r') as f:
    script = f.read().strip()

# Extract character-level timings
characters = alignment['characters']
start_times = alignment['character_start_times_seconds']
end_times = alignment['character_end_times_seconds']

# Combine characters into words
words = script.split()
current_word = ""
word_timings = []
word_start_time = None

char_index = 0

for word in words:
    word_start_time = None
    word_end_time = None
    reconstructed_word = ""
    
    # Iterate through characters to find timings
    while char_index < len(characters) and reconstructed_word != word:
        char = characters[char_index]
        
        # Handle spaces
        if char == " ":
            char_index += 1
            continue
        
        if word_start_time is None:
            word_start_time = start_times[char_index]
        
        reconstructed_word += char
        word_end_time = end_times[char_index]
        char_index += 1
    
    # Append word timings
    if reconstructed_word == word:
        word_timings.append({
            "word": word,
            "start_time": word_start_time,
            "end_time": word_end_time
        })

# Save word timings to a JSON file
with open(output_file, 'w') as f:
    json.dump(word_timings, f, indent=4)

print(f"Word timings saved to {output_file}")
