import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

VIDEOS_PATH = './Filmati/'
MINUTES_PATH = './Minuti/'
OUTPUT_PATH  = "./Output/"
BANNER_PATH = "./Banner/"
CLIPS_PATH = "./"

BANNER_TIME = 3
SECONDS_BEFORE = 5
SECONDS_AFTER = 2

#I need this function to pick up every file with a particular extension
#in the folder that i give as input
def read_file(extension, path):
    quarters = []
    for file in os.listdir(path):
        if file.lower().endswith(extension):
            quarters.append(file)
    print(f"[Console] Trovati {len(quarters)} file che finiscono con {extension}")
    return quarters

def read_clips(clips_name, clips_path):
    clips = []
    for i in range(0, len(clips_name)):
        video = VideoFileClip(clips_path + clips_name[i])
        clips.append(video)
    return clips

#Clips Concatenations
clips = read_clips(read_file("mp4", CLIPS_PATH), CLIPS_PATH)
conc_clips = concatenate_videoclips(clips)

#Banner Composition
banner_path = read_file('png', BANNER_PATH)
banners_videos = [conc_clips]

for i in range(BANNER_TIME, int(conc_clips.duration-BANNER_TIME), BANNER_TIME):
    banners_videos.append((ImageClip(BANNER_PATH + banner_path[int(((i-BANNER_TIME)/BANNER_TIME)%len(banner_path))])
        .set_start(i)
        .set_duration(BANNER_TIME)
        .resize(height=80)
        .margin(top=15, opacity=0)
        .set_pos(("center","top"))))

#Final composition and output
final_sponsor = CompositeVideoClip(banners_videos)
final_sponsor.write_videofile("Highlights.mp4")

for i in range (0, len(clips)):
    clips[i].close()