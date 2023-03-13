import cv2 as cv
import numpy as np


class MaskMapping:
    def __init__(self):
        """Match each BGR color in the original annotation to its mask counterpart.
        CHOICES:
        54: PSM dark grey
            - 125:  arm joint
            - 89:   gripper light grey
            - 87:   needle
            - 0:    thread
            - 104:  background
        """

        self.color_scheme = [54, 125, 89, 87, 0]

        self.mask = [
            {54: 225, 125: 225, 89: 225, 87: 225, 0: 225},
            {54: 225, 125: 225, 89: 225, 87: [0, 80, 250], 0: [0, 250, 80]},
            {54: 225, 125: 225, 89: [250, 250, 0], 87: [0, 80, 250], 0: [0, 250, 80]}
        ]


class ImageCustom:

    def __init__(self, img_name):
        self._width = 1280
        self._height = 480
        self._size = (int(self._width / 2), self._height)

        self.frame = np.zeros((self._width, self._height, 3), dtype="uint8")
        self.image = cv.imread(img_name)
        self._name = img_name

        self.seg_str, self.seg_int = self.seg_name(self.__str__())

        self.img_map = MaskMapping()

    def get_width(self):
        return int(self._width / 2)

    def get_height(self):
        return self._height

    def shape(self):
        """
        return the shape of the image
        :return: [row, col, channel]
        """
        return self._size, 3

    def __str__(self):
        """
        :return: image file name
        """
        return self._name

    def seg_name(self, file_name):
        """
        name in format 2023-xx-xx_xx-xx-xx_0000xxx.png
        :param file_name: image name
        :return: date, time, number
        """
        file_name.strip('.png')
        num = file_name[0:-7]
        num_int = int(num)
        return num, num_int

    def __get_annotation_pixel(self, x, y):
        """
        identify the instrument, thread, and needle according to BGR color for a single pixel
        :param x: the row of the pixel
        :param y: the col of the pixel
        :return: the BGR value of the pixel or -1 if it is part of the background
        """
        B = self.item(x, y, 0)
        G = self.item(x, y, 1)
        R = self.item(x, y, 2)

        for color in self.img_map.color_scheme:
            if B == color and G == color and R == color:
                return color
        return -1

    def set_annotation(self, choice=None):
        """
        #1: black-white (PSM arms/grippers, needle, thread = white [0,1,2,3,4]), the rest are black
        #2: black-3 colors (PSM arms/grippers = white[0,1,2], needle = blue[3], thread = green[4]), the rest are black
        #3: black-4 colors (PSM arms = white[0,1], PSM grippers = purple[2], needle = blue[3], thread = green[4]), the rest are black
        :param choice: 1, 2, 3
        :return: cv::Mat
        """
        if choice is None:
            choice = [0, 1, 2]

        w = self._width
        h = self._height

        new_frame = np.zeros((w, h, 3), dtype="uint8")

        for i in range(0, h):
            for j in range(int(w / 2), w):
                ans = self.__get_annotation_pixel(self, i, j)
                if ans == -1:
                    new_frame[i, j, :] = [0, 0, 0]
                else:
                    mask = self.img_map.mask[choice][ans]
                    if not isinstance(mask, np.ndarray):
                        mask = np.ndarray(mask)
                    if mask.size is not 3:
                        mask = np.append(mask, mask)
                    new_frame[i, j, :] = list(mask)

        return new_frame[:, int(w / 2):w, :]
