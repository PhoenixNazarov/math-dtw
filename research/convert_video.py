import json
import os

import cv2
import numpy as np

from_dir = '../data/signature_video/true/'
to_dir = '../data/signature_coord/true/'

files = os.listdir(from_dir)


def convert_video(from_path, to_path):
    cap = cv2.VideoCapture(from_path)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        return

    before_frame = None
    start = False
    sh = 1
    c = 0

    massive = []
    while (cap.isOpened()):
        ret, frame = cap.read()

        c += 1
        if c % sh != 0:
            continue

        if ret == True:
            binary_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            d_frame = cv2.dilate(binary_frame, np.ones((3, 3), 'uint8'), iterations=1)
            blur_frame = cv2.blur(d_frame, (3, 3))

            if not start:
                sum = 0
                for i in range(frame.shape[0]):
                    for j in range(frame.shape[1]):
                        if binary_frame[i, j] < 128:
                            sum += 1
                if sum > 1:
                    start = 1
                continue

            if before_frame is not None:
                r_frame = cv2.subtract(d_frame, before_frame)
                r_frame = cv2.dilate(r_frame, np.ones((5, 5), 'uint8'), iterations=2)

                sm = 0
                x_s = 0
                y_s = 0
                for i in range(frame.shape[0]):
                    for j in range(frame.shape[1]):
                        if r_frame[i, j] > 4:
                            r_frame[i, j] = 255
                            sm += 1
                            y_s += i
                            x_s += j
                if sm < 1000 and sm != 0:
                    x_s = x_s / sm
                    y_s = y_s / sm
                    massive.append((x_s, y_s))
                else:
                    if len(massive) == 0:
                        massive.append((0, 0))
                    else:
                        massive.append(massive[-1])

            before_frame = d_frame
        else:
            break

    with open(to_path, 'w') as file:
        file.write(json.dumps(massive))


c = 1
for i in files:
    print('start convert', i)
    convert_video(from_dir + i, to_dir + str(c) + '.json')
    c += 1
