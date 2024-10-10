import os
from typing import List
from moviepy.editor import VideoFileClip


def read_files(extension: str, path: str) -> List[str]:
    """
    Retrieve all files with a specific extension from the provided directory.
    """
    files = []
    for file in os.listdir(path):
        if file.lower().endswith(extension):
            files.append(file)
    print(f"[Console] Found {len(files)} files ending with {extension} in {path}")
    return files

def load_clips(clip_names: List[str], clip_path: str) -> List[VideoFileClip]:
    """
    Load video clips from given file names and path.
    """
    clips = []
    for clip_name in clip_names:
        clip_file_path = os.path.join(clip_path, clip_name)
        video = VideoFileClip(clip_file_path)
        clips.append(video)
    return clips

def string_to_seconds(time_str: str) -> int:
    """
    Convert a time string in the format of 'H:M:S', 'M:S', or 'S' into seconds.
    
    Args:
        time_str (str): Time string in one of the formats: 'H:M:S', 'M:S', or 'S'.
        
    Returns:
        int: Total time in seconds.
    """
    time_parts = time_str.split(':')
    
    # Handle cases with different lengths of time parts (H:M:S, M:S, S)
    try:
        if len(time_parts) == 1:  # Seconds only
            s = int(time_parts[0])
            return s
        elif len(time_parts) == 2:  # Minutes:Seconds
            m, s = map(int, time_parts)
            return m * 60 + s
        elif len(time_parts) == 3:  # Hours:Minutes:Seconds
            h, m, s = map(int, time_parts)
            return h * 3600 + m * 60 + s
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    except ValueError as e:
        print(f"Error: {e}")
        raise
