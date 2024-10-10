import os
import yaml
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip 
from utils import read_files, string_to_seconds


def main():
    # Load YAML configuration file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Read video, minutes, and banner paths
    videos_path = read_files('mp4', config['videos_path'])
    minutes_path = read_files('txt', config['minutes_path'])

    # Check if the number of videos and minutes files match
    if len(videos_path) != len(minutes_path):
        raise ValueError(f"Mismatch between the number of videos ({len(videos_path)}) and minutes files ({len(minutes_path)}).")

    final_clips_name = []

    for i in range(len(videos_path)):
        # Obtain minutes and convert to list of seconds
        with open(os.path.join(config['minutes_path'], minutes_path[i]), "r") as f:
            this_video_minutes = f.read().split()

        all_seconds = [string_to_seconds(time_str) for time_str in this_video_minutes]

        # Generate clips from the video based on the time intervals
        video = VideoFileClip(os.path.join(config['videos_path'], videos_path[i]))

        for j, start_time in enumerate(all_seconds):
            clip_name = f"clip-{str(len(final_clips_name)).zfill(2)}.mp4"
            print(clip_name)
            print(f"Video dimensions: {video.size}")  # This should print the width and height of the video

            video.subclip(max(0, start_time - config['seconds_before']),
                          start_time + config['seconds_after']).write_videofile(
                          os.path.join(config['output_path'], clip_name), audio_codec='aac')
            final_clips_name.append(clip_name)

        video.close()

if __name__ == "__main__":
    main()
