import cv2
import numpy as np

cap = cv2.VideoCapture('../data/signature_video/false/2.mp4')


if (cap.isOpened() == False):
    print("Error opening video stream or file")

before_frame = None
start = False
sh = 1
c = 0

massive = []
test_frame = None
while (cap.isOpened()):
    ret, frame = cap.read()

    if test_frame is None:
        test_frame = frame

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
            print(sm)
            if sm < 1000 and sm != 0:
                x_s = x_s / sm
                y_s = y_s / sm
                test_frame = cv2.circle(test_frame, (int(x_s), int(y_s)), radius=1, color=(0, 0, 255), thickness=1)
                massive.append((x_s, y_s))
            else:
                massive.append(massive[-1])


        else:
            r_frame = d_frame

        cv2.imshow('Frame', r_frame)
        cv2.imshow('Frame2', d_frame)
        cv2.imshow('Frame3', test_frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        before_frame = d_frame
    else:
        break

print(massive)

cap.release()
cv2.destroyAllWindows()
