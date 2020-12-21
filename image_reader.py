from PIL import Image
import pytesseract
import numpy as np
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageReader:
    work_path = './out/'
    input_path = './input/'

    def __init__(self, image_file, save_intermediate = False):
        self.image_file = image_file.split('.')[0]
        self.extention = '.' + image_file.split('.')[1]
        self.save_intermediate = save_intermediate
        self.img = cv2.imread(self.input_path + image_file)
        self.grayscale()

    def image_to_bom(self):
        h_grid, v_grid = self.find_image_grid()
        bom_lines = self.image_to_text([h_grid, v_grid])

        return bom_lines

    def image_to_text(self, splits):
        whitelist = '''aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890\\ ,\\/-\\'\\"'''
        conf = f'-c tessedit_char_whitelist={whitelist} psm 13'
        line_splits = splits[0]
        col_splits = splits[1]
        text_font = []
        image_text = []
        for j in range(len(line_splits)-1):
            y1 = line_splits[j]
            y2 = line_splits[j+1]
            line_text = []
            for i in range(len(col_splits)-1):
                x1 = col_splits[i]
                x2 = col_splits[i+1]
                bom_entry = self.gray[y1:y2,x1:x2]
                #line_images.append(bom_line)
                # Trouver un moyen de tester juste les chiffres,
                if self.save_intermediate:
                    file_name = f'{self.work_path}{self.image_file}_l{j+1}_c{i+1}{self.extention}'
                    cv2.imwrite(file_name, bom_entry)
                    entry_text = pytesseract.image_to_string(Image.open(file_name), config=conf)

                else:
                    file_name = f'{self.work_path}{os.getpid()}.jpg'
                    cv2.imwrite(file_name, bom_entry)
                    entry_text = pytesseract.image_to_string(Image.open(file_name), config=conf)
                    os.remove(file_name)

                #print(f'Line {j+1}, col {i+1} = {repr(entry_text)}')
                line_text.append(entry_text.replace('\x0c', '').replace('\n', ''))

            image_text.append(line_text)

        return image_text

    def find_image_grid(self):
        self.height, self.width = self.gray.shape

        split_image = self.detect_rectangles()

        return [0, 0]

    def grayscale(self):
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        if self.save_intermediate:
            file_name = self.work_path + self.image_file + '_gray' + self.extention
            cv2.imwrite(file_name, self.gray)
            print(f'Gray file saved to {self.work_path}')

    def detect_rectangles(self):
        ret, thresh = cv2.threshold(self.gray, 127, 255, 0)
        if self.save_intermediate:
            file_name = self.work_path + self.image_file + '_threshold' + self.extention
            cv2.imwrite(file_name, thresh)
            print(f'Thresh file saved to {self.work_path}')

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        bounding_rect = []
        for c in contours:
            bounding_rect.append(cv2.boundingRect(c))
        print(bounding_rect[1:10])

        contour_img = cv2.drawContours(self.img, contours, -1, (0,0,255), 2)
        if self.save_intermediate:
            file_name = self.work_path + self.image_file + '_contours' + self.extention
            cv2.imwrite(file_name, contour_img)
            print(f'Contour file saved to {self.work_path}')

    def get_grid_dimensions(self, lines, center_splits):
        h_delimiters = []
        v_delimiters = []

        h_grid_lines = []
        v_grid_lines = []
        for l in lines:
            x3, y3, x4, y4 = l[0]

            is_horizontal = y3==y4
            is_vertical = x3==x4

            if is_horizontal and not y3 in h_delimiters:
                h_delimiters.append(y3)
                h_grid_lines.append([0, y3, self.width, y3])

            if is_vertical and not x3 in v_delimiters:
                v_delimiters.append(x3)
                v_grid_lines.append([x3, 0, x3, self.height])

        if center_splits:
            if len(h_delimiters) > 2:
                min_dy = min([j-i for i, j in zip(h_delimiters[:-1], h_delimiters[1:])])
                h1 = 0
                for h in h_delimiters:
                    if h - h1 == min_dy:
                        h_delimiters.remove(h)
                    h1 = h
            if len(v_delimiters) > 2:
                min_dx = min([j-i for i, j in zip(v_delimiters[:-1], v_delimiters[1:])])
                v1 = 0
                for v in v_delimiters:
                    if v - v1 == min_dx:
                        v_delimiters.remove(v)
                    v1 = v

        if self.save_intermediate:
            gridded = self.img.copy()
            h_color = (0, 0, 255)
            v_color = (0, 255, 0)
            for hl in h_grid_lines:
                cv2.line(gridded, (hl[0], hl[1]), (hl[2],hl[3]), h_color, 2, cv2.LINE_AA)

            for vl in v_grid_lines:
                cv2.line(gridded, (vl[0], vl[1]), (vl[2], vl[3]), v_color, 2, cv2.LINE_AA)

            file_name = self.work_path + self.image_file + '_grid' + self.extention
            cv2.imwrite(file_name, gridded)
            print(f'Gridded saved to {self.work_path}')

        return sorted(h_delimiters), sorted(v_delimiters)

if __name__== "__main__":
    save_intermediate = True
    for i in range(3):
        img_file = 'iso'+str(i)+'.png'
        reader = ImageReader(img_file, save_intermediate)
        a = reader.detect_rectangles()





        # col_width = [0]*len(img_text[0])
        # for l in img_text:
        #     for c in range(len(l)):
        #         if len(l[c]) > col_width[c]:
        #             col_width[c] = len(l[c])
        #
        #
        # with open(f'out/out_{i}.txt', 'w') as f:
        #     for l in reader.image_to_bom():
        #         line = ''
        #         for c in range(len(l)):
        #             line += str(l[c]).center(col_width[c] + 2, ' ')
        #             line += ' | '
        #         f.write(line + '\n')
