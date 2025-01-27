import os
import json
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

def create_video_with_scenes(image_folder, audio_file, background_music_file, scenes_file, word_timing_file, output_file):
    # Load JSON file for scenes timing
    with open(scenes_file, 'r') as f:
        scenes_data = json.load(f)

    # Load JSON file for word timings
    with open(word_timing_file, 'r') as f:
        word_timings = json.load(f)

    # Get list of images
    images = sorted([f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))], key=lambda x: int(os.path.splitext(x)[0]))

    # Create an empty list to store all image clips
    video_clips = []

    # Iterate over scenes to create image clips with the respective timing
    for scene_key, scene_timing in scenes_data.items():
        image_file = f"{scene_key}.png"
        image_path = os.path.join(image_folder, image_file)

        if os.path.exists(image_path):
            scene_start_time = scene_timing.get("scene_start_time")
            scene_end_time = scene_timing.get("scene_end_time")

            if scene_start_time is not None:
                if scene_end_time is None:
                    # If scene_end_time is None, use the duration from the audio file
                    scene_end_time = AudioFileClip(audio_file).duration

                duration = scene_end_time - scene_start_time

                # Create image clip with the specified duration
                image_clip = ImageClip(image_path, duration=duration)
                video_clips.append(image_clip)
            else:
                print(f"Invalid timing for scene {scene_key}")
        else:
            print(f"Image file {image_file} not found for scene {scene_key}")

    # Concatenate all image clips into a single video
    if video_clips:
        # Ensure the last image is included fully by adding a small buffer duration if needed
        if len(video_clips) > 1:
            last_clip = video_clips[-1]
            video_clips[-1] = last_clip.set_duration(last_clip.duration + 0.1)

        final_video = concatenate_videoclips(video_clips, method='compose')

        # Load audio clips
        audio_clip = AudioFileClip(audio_file)
        background_music = AudioFileClip(background_music_file).subclip(0, audio_clip.duration).volumex(0.2)
        background_music = background_music.audio_fadeout(3)  # Fade out the background music at the end

        # Set the audio to the final video
        final_audio = CompositeAudioClip([audio_clip, background_music])
        final_video = final_video.set_audio(final_audio)

        # Set the video format and fps
        final_video = final_video.set_fps(24)

        # Create subtitles from word timings (2 words at a time)
        subtitle_entries = []
        for i in range(0, len(word_timings), 2):
            word_1 = word_timings[i]
            word_2 = word_timings[i + 1] if i + 1 < len(word_timings) else None

            start_time = word_1["start_time"]
            end_time = word_2["end_time"] if word_2 else word_1["end_time"]

            text = word_1["word"].upper()
            if word_2:
                text += f" {word_2['word'].upper()}"

            subtitle_entries.append(((start_time, end_time), text))

        # Create a function to generate text clips for subtitles
        def subtitle_generator(txt, color='#00C11D', fontsize=60):
            return TextClip(txt, fontsize=fontsize, color=color, stroke_color='black', stroke_width=2, font='GILLUBCD')

        # Create the subtitles clip
        subtitles_clips = []
        for ((start_time, end_time), text) in subtitle_entries:
            words = text.split()
            if len(words) == 2:
                # Create separate clips for each word with color changes
                word_1_clip_first_half = subtitle_generator(words[0], color='#00C11D', fontsize=65).set_start(start_time).set_duration((end_time - start_time) / 2)
                word_2_clip_first_half = subtitle_generator(words[1], color='#E0FF30', fontsize=60).set_start(start_time).set_duration((end_time - start_time) / 2)

                word_1_clip_second_half = subtitle_generator(words[0], color='#E0FF30', fontsize=60).set_start(start_time + (end_time - start_time) / 2).set_duration((end_time - start_time) / 2)
                word_2_clip_second_half = subtitle_generator(words[1], color='#00C11D', fontsize=65).set_start(start_time + (end_time - start_time) / 2).set_duration((end_time - start_time) / 2)

                # Combine the two word clips with a fixed gap of 7 px
                total_width_first_half = word_1_clip_first_half.w + word_2_clip_first_half.w + 7
                total_width_second_half = word_1_clip_second_half.w + word_2_clip_second_half.w + 7

                # Center the combined clips
                word_1_clip_first_half = word_1_clip_first_half.set_position((final_video.w / 2 - total_width_first_half / 2, final_video.h - 450))
                word_2_clip_first_half = word_2_clip_first_half.set_position((final_video.w / 2 - total_width_first_half / 2 + word_1_clip_first_half.w + 7, final_video.h - 450))

                word_1_clip_second_half = word_1_clip_second_half.set_position((final_video.w / 2 - total_width_second_half / 2, final_video.h - 450))
                word_2_clip_second_half = word_2_clip_second_half.set_position((final_video.w / 2 - total_width_second_half / 2 + word_1_clip_second_half.w + 7, final_video.h - 450))

                # Add the clips to the subtitles
                subtitles_clips.append(word_1_clip_first_half)
                subtitles_clips.append(word_2_clip_first_half)
                subtitles_clips.append(word_1_clip_second_half)
                subtitles_clips.append(word_2_clip_second_half)
            else:
                # Single word case
                single_word_clip = subtitle_generator(text).set_start(start_time).set_duration(end_time - start_time)
                single_word_clip = single_word_clip.set_position(('center', final_video.h - 500))
                subtitles_clips.append(single_word_clip)

        # Overlay subtitles on the final video
        final_video = CompositeVideoClip([final_video, *subtitles_clips])

        # Write the final video to the output path
        final_video.write_videofile(output_file, codec='libx264', audio_codec='aac')
    else:
        print("No video clips were created.")

if __name__ == "__main__":
    # Folders and file paths
    image_folder = "generated_images"
    audio_file = "full_audio.mp3"  # Main audio file with the entire script
    background_music_file = "background_music.mp3"  # Background music file
    scenes_file = "scenes_timing.json"  # Scene timings file
    word_timing_file = "wordtiming.json"  # Word timings file
    output_file = "final_video.mp4"

    # Create the video with scenes and captions
    create_video_with_scenes(image_folder, audio_file, background_music_file, scenes_file, word_timing_file, output_file)