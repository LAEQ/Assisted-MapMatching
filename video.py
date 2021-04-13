import os
import cv2


class Capture:
    def __init__(self, video_path, tmp_folder):
        self.video_path = video_path
        self.tmp_folder = tmp_folder
        self.video_cap = cv2.VideoCapture(video_path)

    def write(self, timestamp, name) -> True:
        self.video_cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        success, image = self.video_cap.read()
        img_path = os.path.join(self.tmp_folder, "{}.jpg".format(name))

        return cv2.imwrite(img_path, image)
