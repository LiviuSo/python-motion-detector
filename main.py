import cv2
import time

from emailing import send_email

video = cv2.VideoCapture(0)

time.sleep(1)

first_frame = None
status_list = [0]
while True:
    status = 0
    # read the frame
    check, frame = video.read()

    # gray the frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

    # blur the frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # save the first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # create a delta frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # create the modulated frame
    threshold_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Dilate the frame
    dil_frame = cv2.dilate(threshold_frame, None, iterations=2)

    # Create contour around main moving object
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 8000:
            continue
        else:
            # object detected
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h),
                                      (0, 255, 0), 3)
            if rectangle.any():
                status = 1

    # update the statues
    status_list.append(status)

    # detect exit and send email
    last_two = status_list[-2:]
    if last_two[0] == 1 and last_two[1] == 0:
        send_email()

    # show the capture (optional)
    cv2.imshow("Video", frame)

    # quit on pressing 'q'
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
