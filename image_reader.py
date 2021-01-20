import pytesseract
import numpy as np
import cv2
from PIL import Image

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

    def threshold(self, img, adaptive=False):
        if adaptive:
            thresh = cv2.adaptiveThreshold(img, 255, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)
        else:
            _, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
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

    def filter_coordinates(self, box_coordinates, filter=0.75, axis=2):
        ws = box_coordinates[:, axis]
        unique_w, freq_w = np.unique(ws, return_counts=True)
        filtered_w = unique_w[freq_w>filter*np.max(freq_w)]

        box_coordinates = box_coordinates[np.isin(ws, filtered_w)]
        return box_coordinates

    def coordinates_to_table(self, box_coordinates, tol=3):
        xs = box_coordinates[:, 0]
        ys = box_coordinates[:,1]
        widths = box_coordinates[:,2]
        heights = box_coordinates[:,3]

        unique_x0 = xs[~(np.triu(np.abs(xs[:, None] - xs) <= tol, 1)).any(0)]
        unique_widths = widths[~(np.triu(np.abs(xs[:, None] - xs) <= tol, 1)).any(0)]
        sorted_indices = np.argsort(unique_x0)
        unique_x0 = unique_x0[sorted_indices]
        unique_widths = unique_widths[sorted_indices]

        unique_y0 = ys[~(np.triu(np.abs(ys[:, None] - ys) <= tol, 1)).any(0)]
        unique_heights = heights[~(np.triu(np.abs(ys[:, None] - ys) <= tol, 1)).any(0)]
        sorted_indices = np.argsort(unique_y0)
        unique_y0 = unique_y0[sorted_indices]
        unique_heights = unique_heights[sorted_indices]

        return [unique_x0, unique_y0, unique_widths, unique_heights]

    def image_to_text_table(self, image_file, hierarchy_level = 1):
        img = self.load_image(image_file, False)
        gray = self.grayscale(img)
        blur = self.blur(gray)
        thresh = self.threshold(blur, True)

        contours = self.find_contours_by_hierarchy(thresh, hierarchy_level)
        box_coordinates = []
        for c in contours:
            box_coordinates.append(cv2.boundingRect(c))

        box_coordinates = self.filter_coordinates(np.array(box_coordinates, dtype='uint16'))
        x, y, w, h = self.coordinates_to_table(box_coordinates)

        print(f'({len(y)} x {len(x)}) table located. Reading text')

        text_table = []
        unwanted_characters = ['\n', '\x0c']
        for j in range(len(y)):
            y0 = y[j]
            y1 = y0 + h[j]
            row = []
            for i in range(len(x)):
                x0 = x[i]
                x1 = x0 + w[i]
                tmp = Image.fromarray(img[y0:y1, x0:x1])
                text = pytesseract.image_to_string(tmp, config='--psm 6')
                for chr in unwanted_characters:
                    text = text.replace(chr, '')
                row.append(text)
            text_table.append(row)

        return text_table

SAVE_INTERMEDIATE = False

if __name__ == '__main__':
    image_reader = ImageReader(SAVE_INTERMEDIATE)
    for n in range(7):
        print(f'Image iso{n}.png content: ')
        image_text_table = image_reader.image_to_text_table(f'./input/iso{n}.png')
        for r in image_text_table:
            print(r)
        print('-'*75 + '\n')


