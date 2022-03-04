import cv2
import imutils
import numpy as np
import datetime
from pathlib import Path

# An idea for a parameter in our future function is whether or not to
# show a visual as the code runs.

detected_images = {}
detected_times = []
videos = []
video_dir = Path("./Videos")
for video_path in video_dir.glob("*.dav"):
    videos.append(str(video_path))
videos.sort()

for video in videos:
    video_dt_format = "%Y%m%d%H%M%S"

    # Offset of 5 seconds - subtract 5 seconds from filename
    videoTimeStamp = datetime.datetime.strptime(video.split("_")[-2], video_dt_format)

    # Video Capture
    capture = cv2.VideoCapture(video)

    # get frames per second
    fps = capture.get(cv2.CAP_PROP_FPS)  # (cv2.CV_CAP_PROP_FPS

    # History, Threshold, DetectShadows
    fgbg = cv2.createBackgroundSubtractorMOG2(300, 100, True)

    # Intialize Average
    avg = None

    # Keeps track of what frame we're on
    frameCount = 0

    while 1:
        # Return Value and the current frame
        ret, frame = capture.read()

        #  Check if a current frame actually exist
        if not ret:
            break

        # Resize the frame
        resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

        # blurs and converts image to grayscale
        gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average frame is None, initialize it
        if avg is None:
            avg = gray.copy().astype("float")
            continue

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 7.5, 255, cv2.THRESH_BINARY)[1]  # 5
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 2500:  # threshold number for contours
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(resizedFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Animal"
            cv2.putText(resizedFrame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            newTime = datetime.timedelta(0, time) + videoTimeStamp
            print(newTime)
            detected_times.append(newTime)
            detected_images[newTime] = resizedFrame

        frameCount += 1
        time = float(frameCount) / fps
        newTime = datetime.timedelta(0, time) + videoTimeStamp
        cv2.putText(resizedFrame, str(newTime), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("Frame", resizedFrame)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    capture.release()
    cv2.destroyAllWindows()

with open("detected_times.txt", "w") as output_file:
    for time in detected_times:
        output_file.write(time.strftime(video_dt_format))
