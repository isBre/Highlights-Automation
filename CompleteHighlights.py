import os
import yaml
from typing import List
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip 
from utils import read_files, load_clips, string_to_seconds


def main():
    # Load YAML configuration file
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Get paths from config
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
            video.subclip(max(0, start_time - config['seconds_before']),
                          start_time + config['seconds_after']).write_videofile(
                          os.path.join(config['output_path'], clip_name), audio_codec='aac')
            final_clips_name.append(clip_name)
        video.close()

    # Clips Concatenations
    clips = load_clips(read_files("mp4", config['clips_path']), config['clips_path'])
    conc_clips = concatenate_videoclips(clips)
    
    # Close clips after use
    for clip in clips:
        clip.close()

    # Banner Composition
    banner_files = read_files('png', config['banner_path'])
    banners_videos = [conc_clips]

    for i in range(config['banner_time'], int(conc_clips.duration - config['banner_time']), config['banner_time']):
        banner_img = ImageClip(os.path.join(config['banner_path'], banner_files[i % len(banner_files)]))
        banner_clip = (banner_img.set_start(i)
                               .set_duration(config['banner_time'])
                               .resize(height=80)
                               .margin(top=15, opacity=0)
                               .set_pos(("center", "top")))
        banners_videos.append(banner_clip)

    # Final composition and output
    final_sponsor = CompositeVideoClip(banners_videos)
    final_sponsor.write_videofile(os.path.join(config['output_path'], "Highlights.mp4"))

if __name__ == "__main__":
    main()