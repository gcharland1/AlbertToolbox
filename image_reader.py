from PIL import Image
import pytesseract
import numpy as np
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageReader:
    def __init__(self, save_intermediate = False, output_path = './out/'):
        self.img = None
        self.save = save_intermediate
        self.save_dir = output_path

    def load_image(self, image_file):
        self.img = cv2.imread(image_file, 0)

        if self.save:
            cv2.imwrite(self.save_dir + 'original.png', self.img)

    def invert_image(self):
        self.threshold, self.img_bin = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY)
        self.inverted = 255-self.img_bin

        if self.save:
            cv2.imwrite(self.save_dir + 'bin.png', self.inverted)

    def detect_grid(self):
        self.invert_image()
        # Defining a kernel length
        kernel_length = np.array(self.inverted).shape[1] // 80

        # A verticle kernel of (1 X kernel_length), which will detect all the vertical lines from the image.
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))  # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))  # A kernel of (3 X 3) ones.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Morphological operation to detect vertical lines from an image
        img_temp1 = cv2.erode(self.inverted, verticle_kernel, iterations=3)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(self.inverted, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

        if self.save:
            cv2.imwrite(self.save_dir + "verticle_lines.jpg", verticle_lines_img)
            cv2.imwrite(self.save_dir + "horizontal_lines.jpg", horizontal_lines_img)


SAVE_INTERMEDIATE = True

if __name__ == '__main__':
    image_reader = ImageReader(SAVE_INTERMEDIATE)
    image_reader.load_image('./input/iso0.png')
    image_reader.detect_grid()