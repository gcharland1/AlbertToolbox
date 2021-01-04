from PIL import Image
import pytesseract
import numpy as np
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageReader:
    def __init__(self, save_intermediate = False, output_path = './out/'):
        self.img = None
        self.loaded_image = False
        self.save = save_intermediate
        self.save_dir = output_path

    def load_image(self, image_file):
        try:
            self.img = cv2.imread(image_file, 0)
            self.loaded_image = True
            if self.save:
                cv2.imwrite(self.save_dir + 'original.png', self.img)
        except:
            self.loaded_image = False
            print('Invalid image file. Double check please')

        return self.loaded_image


    def invert_image(self):
        if self.loaded_image:
            self.threshold, self.img_bin = cv2.threshold(self.img, 127, 255, cv2.THRESH_BINARY)
            self.inverted = 255-self.img_bin

            if self.save:
                cv2.imwrite(self.save_dir + 'bin.png', self.inverted)
        else:
            print('No image loaded. Use ImageReader.load_image("image_file") first')

    def detect_grid(self, image_file=""):
        if not self.loaded_image: # Try to load image
            self.load_image(image_file)

        if self.loaded_image:
            self.invert_image()

            # Defining a kernel length
            kernel_length = np.array(self.inverted).shape[1] // 80

            # A vertical kernel of (1 X kernel_length), which will detect all the vertical lines from the image.
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))  # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
            hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))  # A kernel of (3 X 3) ones.
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            # Morphological operation to detect vertical lines from an image
            img_temp1 = cv2.erode(self.inverted, vertical_kernel, iterations=3)
            vertical_lines_img = cv2.dilate(img_temp1, vertical_kernel, iterations=3)

            # Morphological operation to detect horizontal lines from an image
            img_temp2 = cv2.erode(self.inverted, hori_kernel, iterations=3)
            horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)

            # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
            alpha = 0.5
            beta = 1.0 - alpha  # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
            img_final_bin = cv2.addWeighted(vertical_lines_img, alpha, horizontal_lines_img, beta, 0.0)
            img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
            (thresh, self.grid_img_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


            if self.save:
                cv2.imwrite(self.save_dir + "vertical_lines.jpg", vertical_lines_img)
                cv2.imwrite(self.save_dir + "horizontal_lines.jpg", horizontal_lines_img)
                cv2.imwrite(self.save_dir + "img_final_bin.jpg", self.grid_img_bin)
        else:
            print('No image loaded. Use ImageReader.load_image("image_file") or ImageReader.detect_grid("image_file")')





SAVE_INTERMEDIATE = True

if __name__ == '__main__':
    image_reader = ImageReader(SAVE_INTERMEDIATE)
    image_reader.detect_grid('./input/iso0.png')