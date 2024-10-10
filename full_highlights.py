import os
from moviepy.editor import concatenate_videoclips, CompositeVideoClip
from utils import (read_files, load_clips, string_to_seconds, load_config, 
                   generate_clips, create_banner_clips)

def main():
    config = load_config('config.yaml')

    videos_path = read_files('mp4', config['videos_path'])
    minutes_path = read_files('txt', config['minutes_path'])

    if len(videos_path) != len(minutes_path):
        raise ValueError(
            f"Mismatch between the number of videos ({len(videos_path)}) "
            f"and minutes files ({len(minutes_path)})."
        )

    final_clips_name = []

    for i, video_file in enumerate(videos_path):
        with open(os.path.join(config['minutes_path'], minutes_path[i]), "r") as f:
            this_video_minutes = f.read().split()

        all_seconds = [string_to_seconds(time_str) for time_str in this_video_minutes]
        final_clips_name += generate_clips(os.path.join(config['videos_path'], video_file), 
                                           all_seconds, config, config['output_path'])

    clips = load_clips(read_files("mp4", config['clips_path']), config['clips_path'])
    conc_clips = concatenate_videoclips(clips)

    banners_videos = create_banner_clips(conc_clips, config, 
                                         read_files('png', config['banner_path']))

    final_sponsor = CompositeVideoClip(banners_videos)
    final_sponsor.write_videofile(os.path.join(config['output_path'], "Highlights.mp4"))

if __name__ == "__main__":
    main()
