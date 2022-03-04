import cv2
import imutils
import numpy as np
import datetime

videos = ["LNR408_ch2_main_20180726065707_20180726065726.dav", "LNR408_ch2_main_20180726063934_20180726064007.dav"]
videos.sort()
current_video = "Videos/LNR408_ch0_main_20180726065707_20180726065726.dav.mp4"
video_dt_format = "%Y%m%d%H%M%S"
videoTimeStamp = datetime.datetime.strptime(current_video.split("_")[-2], video_dt_format)


# Video Capture 
# capture = cv2.VideoCapture(0)
#capture = cv2.VideoCapture("Videos/natureClip.mp4")
#capture = cv2.VideoCapture("Videos/Caterpiller.mp4")
capture = cv2.VideoCapture(current_video)
#capture = cv2.VideoCapture("Videos/LNR408_ch2_main_20180726063934_20180726064007.dav")
#capture = cv2.VideoCapture("Videos/LNR408_ch2_main_20180726065707_20180726065726.dav")
# Offset of 5 seconds - subtract 5 seconds from filename

#get frames per second
fps = capture.get(cv2.CAP_PROP_FPS) #(cv2.CV_CAP_PROP_FPS

# History, Threshold, DetectShadows 
# fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)
fgbg = cv2.createBackgroundSubtractorMOG2(300, 100, True)

#Intialize Average
avg = None

# Keeps track of what frame we're on
frameCount = 0

while(1):
	# Return Value and the current frame
	ret, frame = capture.read()

	#  Check if a current frame actually exist
	if not ret:
		break

	# Resize the frame
	resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

	#blurs and converts image to grayscale
	gray = cv2.cvtColor(resizedFrame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the average frame is None, initialize it
	if avg is None:
		avg = gray.copy().astype("float")
		#capture.truncate(0)
		continue

	# accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
	cv2.accumulateWeighted(gray, avg, 0.5)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	# threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
	thresh = cv2.threshold(frameDelta, 7.5, 255,
		cv2.THRESH_BINARY)[1] #5
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 2500: #threshold number for contours
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(resizedFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Animal"
		cv2.putText(resizedFrame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
		newTime = datetime.timedelta(0, time) + videoTimeStamp
		print(newTime)

	frameCount += 1
	time = float(frameCount)/fps
	newTime = datetime.timedelta(0, time) + videoTimeStamp
	cv2.putText(resizedFrame, str(newTime), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

	# Get the foreground mask
	#fgmask = fgbg.apply(resizedFrame)

	# Count all the non zero pixels within the mask
	#count = np.count_nonzero(fgmask)

	#print('Frame: %d, FPS: %d, Pixel Count: %d' % (frameCount, fps, count))

	# Determine how many pixels do you want to detect to be considered "movement"
	# if (frameCount > 1 and cou`nt > 5000):

	# if (frameCount > 1 and count > 17000): #experiment with the thresh hold number
	# 	print('Animal detected: %f' % time)
	# 	cv2.putText(resizedFrame, 'Animal detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
	# 	#Output timestamp

	cv2.imshow('Frame', resizedFrame)
	# cv2.imshow('Mask', fgmask)


	k = cv2.waitKey(1) & 0xff
	if k == 27:
		break

capture.release()
cv2.destroyAllWindows()