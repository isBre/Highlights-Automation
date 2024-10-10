import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

VIDEOS_PATH = './Movies/'
MINUTES_PATH = './Minutes/'
OUTPUT_PATH  = "./Output/"
BANNER_PATH = "./Ads/"
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
    print(f"[Console] Trovati {len(quarters)} che finiscono con {extension}")
    return quarters

def read_clips(clips_name, clips_path):
    clips = []
    for i in range(0, len(clips_name)):
        video = VideoFileClip(clips_path + clips_name[i])
        clips.append(video)
    return clips

def string_to_seconds(time_str):
    h, m = (0, 0)
    if len(time_str.split(':')) == 1:
        s = time_str
    elif len(time_str.split(':')) == 2:
        m, s = time_str.split(':')
    else:
        h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


videos_path = read_file('mp4', VIDEOS_PATH)
minutes_path = read_file('txt', MINUTES_PATH)

#If videos and files with minutes are not the same there is a problem
if len(videos_path) != len(minutes_path):
    print('Numero di filmati diverso dal numero di highlights corrispondenti')
    quit()

final_clips_name = []

for i in range(0, len(videos_path)):

    #Obtain minutes and transform that in a list of seconds
    this_video_minutes = open(MINUTES_PATH + minutes_path[i], "r").read().split()
    all_seconds = [0]*len(this_video_minutes)
    for j in range(0, len(this_video_minutes)):
        all_seconds[j] = string_to_seconds(this_video_minutes[j])

    #Generate clips
    video = VideoFileClip(VIDEOS_PATH + videos_path[i])
    for j in range(0, len(all_seconds)):
        clip_name = f"clip-{str(len(final_clips_name)).zfill(2)}.mp4"
        video.subclip(all_seconds[j] - SECONDS_BEFORE, 
            all_seconds[j] + SECONDS_AFTER).write_videofile(clip_name, audio_codec='aac')
        final_clips_name.append(clip_name)
        
    video.close()

#Clips Concatenations
clips = read_clips(read_file("mp4", CLIPS_PATH))
conc_clips = concatenate_videoclips(clips)
for i in range (0, len(clips)):
        clips[i].close()

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