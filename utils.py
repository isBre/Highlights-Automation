import os
import yaml
from moviepy.editor import VideoFileClip, ImageClip
from typing import List


# File handling utilities
def read_files(extension: str, directory: str) -> List[str]:
    """
    Read all files with a specific extension from a directory.
    
    Args:
        extension (str): The file extension to filter by (e.g., 'mp4').
        directory (str): The path to the directory containing files.
    
    Returns:
        List[str]: A list of filenames with the specified extension.
    """
    return [f for f in os.listdir(directory) if f.endswith(f".{extension}")]


def load_config(file_path: str) -> dict:
    """
    Load a YAML configuration file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: The configuration as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Time utilities
def string_to_seconds(time_str: str) -> int:
    """
    Convert a time string (HH:MM:SS, MM:SS, or SS) into seconds.
    
    Args:
        time_str (str): Time as a string in one of the formats:
                        'HH:MM:SS', 'MM:SS', or 'SS'.
    
    Returns:
        int: Time in seconds.
    """
    time_parts = list(map(int, time_str.split(':')))

    # Handle different time formats based on the number of parts
    if len(time_parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = time_parts
    elif len(time_parts) == 2:  # MM:SS
        hours = 0
        minutes, seconds = time_parts
    elif len(time_parts) == 1:  # SS
        hours = 0
        minutes = 0
        seconds = time_parts[0]
    else:
        raise ValueError(f"Invalid time format: {time_str}")

    return hours * 3600 + minutes * 60 + seconds


# Video processing utilities
def load_clips(clip_names: List[str], clips_path: str) -> List[VideoFileClip]:
    """
    Load video clips from a list of filenames.

    Args:
        clip_names (List[str]): List of video filenames.
        clips_path (str): Directory where the clips are stored.

    Returns:
        List[VideoFileClip]: A list of loaded VideoFileClip objects.
    """
    return [VideoFileClip(os.path.join(clips_path, name)) for name in clip_names]


def generate_clips(video_file: str, times: List[int], config: dict, output_path: str) -> List[str]:
    """
    Generate video clips based on start times and duration settings from config.

    Args:
        video_file (str): Path to the video file.
        times (List[int]): List of start times in seconds for each clip.
        config (dict): Configuration dictionary containing 'seconds_before' and 'seconds_after' values.
        output_path (str): Directory where the generated clips will be saved.

    Returns:
        List[str]: A list of filenames of the generated clips.
    """
    video = VideoFileClip(video_file)
    clip_names = []
    
    for i, start_time in enumerate(times):
        clip_name = f"clip-{str(i).zfill(2)}.mp4"
        # Define start and end time for each clip based on config settings
        start = max(0, start_time - config['seconds_before'])
        end = start_time + config['seconds_after']
        
        # Write the subclip to a new file
        video.subclip(start, end).write_videofile(
            os.path.join(output_path, clip_name), audio_codec='aac'
        )
        
        clip_names.append(clip_name)
    
    video.close()
    return clip_names


# Banner handling utilities
def create_banner_clips(concatenated_clip: VideoFileClip, config: dict, banner_files: List[str]) -> List[ImageClip]:
    """
    Overlay banners at regular intervals on a concatenated video clip.

    Args:
        concatenated_clip (VideoFileClip): The main video clip onto which banners will be added.
        config (dict): Configuration dictionary containing 'banner_time' and 'banner_path'.
        banner_files (List[str]): List of banner image filenames.

    Returns:
        List[ImageClip]: A list of ImageClip objects for the banners.
    """
    banner_clips = [concatenated_clip]  # Start with the main video clip

    # Loop through the video duration and place banners at specified intervals
    for i in range(config['banner_time'], int(concatenated_clip.duration - config['banner_time']), config['banner_time']):
        banner_img = ImageClip(os.path.join(config['banner_path'], banner_files[i % len(banner_files)]))
        
        # Customize the banner position, size, and duration
        banner_clip = (banner_img.set_start(i)
                                .set_duration(config['banner_time'])
                                .resize(height=80)
                                .margin(top=15, opacity=0)
                                .set_pos(("center", "top")))
        
        banner_clips.append(banner_clip)

    return banner_clips
