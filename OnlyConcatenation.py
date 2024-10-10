import os
import yaml
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip 
from utils import read_files, load_clips

def main():
    # Load YAML configuration file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Read video clips from the clips path defined in the config
    clips = load_clips(read_files("mp4", config['clips_path']), config['clips_path'])

    # Concatenate all the video clips
    concatenated_clips = concatenate_videoclips(clips)

    # Load banner images (PNG files) from banner path
    banner_files = read_files('png', config['banner_path'])
    banner_clips = [concatenated_clips]

    # Add banners at specified intervals
    for i in range(config['banner_time'], int(concatenated_clips.duration - config['banner_time']), config['banner_time']):
        banner_image = ImageClip(os.path.join(config['banner_path'], banner_files[i % len(banner_files)]))
        banner_clip = (
            banner_image.set_start(i)
            .set_duration(config['banner_time'])
            .resize(height=80)
            .margin(top=15, opacity=0)
            .set_pos(("center", "top"))
        )
        banner_clips.append(banner_clip)

    # Create the final video with banners overlaid
    final_video = CompositeVideoClip(banner_clips)

    # Output the final video file
    output_path = os.path.join(config['output_path'], "Highlights.mp4")
    final_video.write_videofile(output_path)

    # Ensure all clips are properly closed to release resources
    for clip in clips:
        try:
            clip.close()
        except Exception as e:
            print(f"Error closing clip: {e}")

if __name__ == "__main__":
    main()