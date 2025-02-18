import cv2

# Load the video
video_path = 'output.mp4'
cap = cv2.VideoCapture(video_path)

# Set the position of the frame you want to capture (e.g., 5 seconds)
cap.set(cv2.CAP_PROP_POS_MSEC, 5000)  # 5000 milliseconds = 5 seconds

# Read the frame
ret, frame = cap.read()

# Save the frame as an image
if ret:
    cv2.imwrite('carParkThumbnail.png', frame)

cap.release()