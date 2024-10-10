import os
from utils import read_files, string_to_seconds, load_config, generate_clips


def main():
    config = load_config('config.yaml')

    videos_path = read_files('mp4', config['videos_path'])
    minutes_path = read_files('txt', config['minutes_path'])

    if len(videos_path) != len(minutes_path):
        raise ValueError(
            f"Mismatch between the number of videos ({len(videos_path)}) "
            f"and minutes files ({len(minutes_path)})."
        )

    for i, video_file in enumerate(videos_path):
        with open(os.path.join(config['minutes_path'], minutes_path[i]), "r") as f:
            this_video_minutes = f.read().split()

        all_seconds = [string_to_seconds(time_str) for time_str in this_video_minutes]
        generate_clips(os.path.join(config['videos_path'], video_file), 
                       all_seconds, config, config['output_path'])

if __name__ == "__main__":
    main()
