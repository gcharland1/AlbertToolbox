import pytesseract
import numpy as np
import cv2
from matplotlib import pyplot as plt

# if os == Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# else:

class ImageReader:
    def __init__(self, save_intermediate = False, output_path = './out/'):
        self.save = save_intermediate
        self.save_dir = output_path

    def load_image(self, image_file, as_grayscale = False):
        if as_grayscale:
            flag = cv2.IMREAD_GRAYSCALE
        else:
            flag = cv2.IMREAD_COLOR
        img = cv2.imread(image_file, flag)
        return img

    def grayscale(self, img):
        gray_img =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray_img

    def blur(self, img, area=(5, 5)):
        w = area[0]
        h = area[1]
        if w % 2 == 0:
            w = w + 1
        if h % 2 == 0:
            h = h + 1

        blur = cv2.GaussianBlur(img, (w, h), 0)
        return blur

    def threshold(self, img, adaptive=True):
        if adaptive:
            thresh = cv2.adaptiveThreshold(img, 255, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)
        else:
            _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return thresh

    def find_contours(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def find_contours_by_hierarchy(self, img, hierarchy_level=0):
        if hierarchy_level == 0:
            level_contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            children = [-1] # Start with outer most contours
            for level in range(hierarchy_level + 1):
                parents = children # Parents are the previous level children
                children = np.array([], dtype='uint8')
                for parent in parents:
                    children = np.append(children, np.where(hierarchy[0,:,3]==parent)[0])

            contours = np.array(contours, dtype=object)
            level_contours = contours[children]

        return level_contours

    def find_biggest_contour(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        biggest_blob = None
        for c in contours:
            area = cv2.contourArea(c)
            if  area > max_area:
                biggest_blob = c
                max_area = area

        return biggest_blob

    def filter_table(self, box_coordinates):
        return box_coordinates

    def image_to_table(self, image_file):
        img = image_reader.load_image(image_file, False)
        gray = image_reader.grayscale(img)
        blur = image_reader.blur(gray)
        thresh = image_reader.threshold(blur, True)

        hierarchy_level = 1
        contours = image_reader.find_contours_by_hierarchy(thresh, hierarchy_level)
        box_coordinates = []
        for c in contours:
            box_coordinates.append(cv2.boundingRect(c))

        box_coordinates = self.filter_table(np.array(box_coordinates, dtype='uint8'))

        return box_coordinates


SAVE_INTERMEDIATE = False

if __name__ == '__main__':
    image_reader = ImageReader(SAVE_INTERMEDIATE)
    for n in [0, 1, 2]:
        print(image_reader.image_to_table(f'./input/iso{n}.png'))

