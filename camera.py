import glob
import os
import time
from threading import Thread

import cv2

import timeplay
from emailing import send_email


def camera_cv2(frame):
    cv2.imshow("Video", frame)


def notify(image_path, email_receiver):
    send_email(image_path, email_receiver)

    # Clean the frames
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


def run_camera(camera_engine,
               receiver="lvictor1979@gmail.com",
               initial_delay=1):
    video = cv2.VideoCapture(0)

    time.sleep(initial_delay)

    first_frame = None
    status_list = [0]
    count = 1
    while True:
        status = 0
        # read the frame
        check, frame = video.read()

        # gray the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_BGRA2GRAY)

        # blur the frame
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # save the first frame
        if first_frame is None:
            first_frame = gray_frame_gau

        # create a delta frame
        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

        # create the modulated frame
        threshold_frame = \
            cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

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
                # shape delimited
                if rectangle.any():
                    status = 1  # update the status
                    cv2.imwrite(f"images/{count}.png", frame)  # save the frame
                    count = count + 1

        # update the statues
        status_list.append(status)

        # detect exit and send email
        last_two = status_list[-2:]
        if last_two[0] == 1 and last_two[1] == 0:
            # select the screen capture to send
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]
            # send email
            email_thread = Thread(target=notify,
                                  args=(image_with_object, receiver))
            email_thread.daemon = True  # allow execution in background
            email_thread.start()

        # show timestamp
        day, hour = timeplay.get_day_and_time()
        cv2.putText(img=frame, text=day, org=(20, 40),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=(230, 230, 230), thickness=2,
                    lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=hour, org=(20, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=(10, 10, 250), thickness=2,
                    lineType=cv2.LINE_AA)

        # show the capture (optional)
        camera_engine(frame)

        # quit on pressing 'q'
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()


if __name__ == '__main__':
    run_camera(camera_engine=camera_cv2)
