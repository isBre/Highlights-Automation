import os
from moviepy.editor import concatenate_videoclips, CompositeVideoClip
from utils import read_files, load_clips, load_config, create_banner_clips


def main():
    config = load_config('config.yaml')

    clips = load_clips(read_files("mp4", config['clips_path']), config['clips_path'])
    concatenated_clips = concatenate_videoclips(clips)

    banner_files = read_files('png', config['banner_path'])
    banners_videos = create_banner_clips(concatenated_clips, config, banner_files)

    final_video = CompositeVideoClip(banners_videos)
    final_video.write_videofile(os.path.join(config['output_path'], "Highlights.mp4"))

    for clip in clips:
        try:
            clip.close()
        except Exception as e:
            print(f"Error closing clip: {e}")

if __name__ == "__main__":
    main()
