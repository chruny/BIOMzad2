from numpy import linspace

PROGRAM = "Pycharm"
if PROGRAM != "Pycharm":
    from google.colab import drive
import os
import numpy as np
import cv2
import csv

# nacitanie obrazkov
dataroot = '/content/gdrive/My Drive/Colab Notebooks/'


class CSVLine:
    image_name = ''
    center_x_1 = ''
    center_y_1 = ''
    polomer_1 = ''
    center_x_2 = ''
    center_y_2 = ''
    polomer_2 = ''
    center_x_3 = ''
    center_y_3 = ''
    polomer_3 = ''
    center_x_4 = ''
    center_y_4 = ''
    polomer_4 = ''
    image = None

    def __init__(self):
        pass

    def constructor(self, image_name, center_x_1, center_y_1, polomer_1, center_x_2, center_y_2, polomer_2, center_x_3,
                    center_y_3, polomer_3, center_x_4, center_y_4, polomer_4, image):
        self.image_name = image_name
        self.center_x_1 = int(center_x_1)
        self.center_y_1 = int(center_y_1)
        self.polomer_1 = int(polomer_1)

        self.center_x_2 = int(center_x_2)
        self.center_y_2 = int(center_y_2)
        self.polomer_2 = int(polomer_2)

        self.center_x_3 = int(center_x_3)
        self.center_y_3 = int(center_y_3)
        self.polomer_3 = int(polomer_3)

        self.center_x_4 = int(center_x_4)
        self.center_y_4 = int(center_y_4)
        self.polomer_4 = int(polomer_4)

        self.image = image


def get_circle_length(radius):
    return 2 * np.pi * radius


def show(title, image):
    cv2.imshow(title, image)
    cv2.waitKey()


def process_image(image_csv):
    samples = np.linspace(0, np.pi, num=int(get_circle_length(image_csv.polomer_1)))

    center_zr = (image_csv.center_x_1, image_csv.center_y_1)
    center_du = (image_csv.center_x_2, image_csv.center_y_2)
    center_hv = (image_csv.center_x_3, image_csv.center_y_3)
    center_dv = (image_csv.center_x_4, image_csv.center_y_4)

    centerx = np.linspace(center_zr[0], center_du[0], image_csv.polomer_2 - image_csv.polomer_1)
    centery = np.linspace(center_zr[1], center_du[1], image_csv.polomer_2 - image_csv.polomer_1)

    print(len(centerx))
    print(len(centery))

    norm = np.zeros((image_csv.polomer_2 - image_csv.polomer_1, int(get_circle_length(image_csv.polomer_1))))
    polar = np.zeros((image_csv.polomer_2 - image_csv.polomer_1, int(get_circle_length(image_csv.polomer_1))))
    for r in range(image_csv.polomer_2 - image_csv.polomer_1):
        for it, theta in enumerate(samples):
            x = int((r + image_csv.polomer_1) * np.cos(theta) + centerx[r])
            y = int((r + image_csv.polomer_1) * np.sin(theta) + centery[r])
            print(image_csv.image[y][x][0])
            # ak je vlavo
            if x < image_csv.center_x_1:
                polar[r][it] = image_csv.image[y][x][0]
            elif x > image_csv.center_x_1:
                polar[r][it] = image_csv.image[y][x][0]
    show(image_csv.image_name, polar)


def show_image(image_csv):
    print(image_csv.center_x_1)
    print(image_csv.center_y_1)
    print(image_csv.polomer_1)
    # cv2.circle(image2, (i[0], i[1]), i[2], (0, 255, 0), 2)
    print(image_csv.image)
    cv2.circle(image_csv.image, (image_csv.center_x_1, image_csv.center_y_1), image_csv.polomer_1, (0, 255, 0), 2)
    cv2.circle(image_csv.image, (image_csv.center_x_2, image_csv.center_y_2), image_csv.polomer_2, (0, 255, 0), 2)
    cv2.circle(image_csv.image, (image_csv.center_x_3, image_csv.center_y_3), image_csv.polomer_3, (0, 255, 0), 2)
    cv2.circle(image_csv.image, (image_csv.center_x_4, image_csv.center_y_4), image_csv.polomer_4, (0, 255, 0), 2)
    process_image(image_csv)
    # show(image_csv.image_name, image_csv.image)


def load_image(path):
    img = cv2.imread(path)
    if img is not None:
        return img


def load_images():
    if PROGRAM != "Pycharm":
        main_directory = dataroot + "iris_NEW"
    else:
        main_directory = "iris_NEW"
    dirs = os.listdir(main_directory)
    for dir in dirs:
        if os.path.isdir(main_directory + '/' + dir):
            subdirs = os.listdir(main_directory + '/' + dir)
            for subdir in subdirs:
                if os.path.isdir(main_directory + '/' + dir + '/' + subdir):
                    imgs = os.listdir(main_directory + '/' + dir + '/' + subdir)
                    for img in imgs:
                        if '.jpg' in img:
                            print(dir + '/' + subdir + '/' + img)


def load_csv():
    csv_file = {}
    if PROGRAM != "Pycharm":
        path = dataroot + 'iris_NEW/iris_bounding_circles.csv'
        main_directory = dataroot + "iris_NEW"
    else:
        path = 'iris_NEW/iris_bounding_circles.csv'
        main_directory = "iris_NEW"

    with open(path) as file:
        reader = csv.reader(file, delimiter=',')
        for i, line in enumerate(reader):
            if i > 0:
                line_csv = CSVLine()
                line_tmp = line[0].replace('_n2', '')
                image = load_image(main_directory + '/' + line[0])
                line_csv.constructor(line_tmp, line[1], line[2], line[3], line[4], line[5], line[6],
                                     line[7],
                                     line[8], line[9], line[10], line[11], line[12], image)
                show_image(line_csv)
                csv_file[line_tmp] = line_csv
    return csv_file


# drive.mount('/content/gdrive')
print("Loading Image")
load_images()
print("Loading CSV")
load_csv()
print("End")
