import string
import cv2
import random

# cap = cv2.VideoCapture('C:\\MKA\\demo video\\for_testing.mp4')
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

ret, frame1 = cap.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

ascii_chars = list(string.punctuation + "@#$%^&*()+=<>?/|~")
font = cv2.FONT_HERSHEY_DUPLEX
font_scale = 0.35
font_thickness = 1

ascii_cols = frame_width // 10
ascii_rows = frame_height // 15


ascii_buffer = []
buffer_size = 12

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
    diff = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    scaled_thresh = cv2.resize(thresh, (ascii_cols, ascii_rows))
    scaled_gray = cv2.resize(gray2, (ascii_cols, ascii_rows))
    ascii_frame = []
    for i, row in enumerate(scaled_gray):
        ascii_row = []
        for j, pixel in enumerate(row):
            if scaled_thresh[i, j] > 0:
                ascii_row.append(
                    random.choice(ascii_chars[:min(pixel // 5 + 1, len(ascii_chars))]))
            else:
                ascii_row.append(' ')
        ascii_frame.append(ascii_row)

    if len(ascii_buffer) >= buffer_size:
        ascii_buffer.pop(0)
    ascii_buffer.append(ascii_frame)
    counter = 0
    for buffer_frame in ascii_buffer:
        if counter%3 == 0:
            counter = counter + 1
            for i, row in enumerate(buffer_frame):
                for j, char in enumerate(row):
                    if char != ' ':
                        cv2.putText(frame2, char, (j * 10, i * 15), font, font_scale, (255,0,255), font_thickness)
        else:
            counter = 0

    out.write(frame2)

    cv2.imshow("ASCII Motion Tracking", frame2)

    gray1 = gray2

    # Press if 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

