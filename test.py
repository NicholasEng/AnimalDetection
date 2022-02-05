#print("Hello World!")

import datetime

videos = ["LNR408_ch2_main_20180726065707_20180726065726.dav", "LNR408_ch2_main_20180726063934_20180726064007.dav"]
videos.sort()
current_video = "Videos/LNR408_ch2_main_20180726065707_20180726065726.dav"
video_dt_format = "%Y%m%d%H%M%S"
videoTimeStamp = datetime.datetime.strptime(current_video.split("_")[-2], video_dt_format)


fps = 30
frames = 40

time = frames/fps

print(videoTimeStamp)
newTime = datetime.timedelta(0, time) + videoTimeStamp
print(newTime)