import pytesseract
import numpy as np
import cv2

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

    def blur(self, img):
        blur = cv2.GaussianBlur(img, (5, 5), 0)
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

    def mask_outer_perimeter(self, shape, contours, min_area):
        best_contour = None
        max_area = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area > min_area:
                if area > max_area:
                    max_area = area
                    best_contour = c


        mask = np.zeros(shape, np.uint8)
        cv2.drawContours(mask, [best_contour], 0, 255, -1)
        cv2.drawContours(mask, [best_contour], 0, 0, 2)
        return mask

    def draw_coutours(self, img, contours, min_area = 500):
        c = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > min_area:
                cv2.drawContours(img, contours, c, (0,255,0), 3)
            c += 1
        return img

    def isolate_outer_box_content(self, img, min_area = 500):
        gray = self.grayscale(img)
        blur = self.blur(gray)
        thresh = self.threshold(blur, True)
        contours = self.find_contours(thresh)
        mask = self.mask_outer_perimeter(gray.shape, contours, min_area)

        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]
        return out

SAVE_INTERMEDIATE = True

if __name__ == '__main__':
    image_reader = ImageReader(SAVE_INTERMEDIATE)
    for n in [0, 1, 2]:
        img = image_reader.load_image(f'./input/iso{n}.png', False)
        print(f'./input/iso{n}.png')
        gray = image_reader.grayscale(img)
        blur = image_reader.blur(gray)
        thresh = image_reader.threshold(blur, True)

        for level in [0, 1]:
            contours = image_reader.find_contours_by_hierarchy(thresh, level)

            cv2.drawContours(img, contours, -1, (0,255,0), 2)
            cv2.imwrite(f'./out/iso{n}_level{level}.png', img)
