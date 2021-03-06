import math
import os
from os.path import isfile
from os.path import join
import sys
import cv2
import matplotlib as mpl
mpl.use('TkAgg')
import numpy as np
from matplotlib import pyplot as plt
from amazon import upload_toS3

_DEFAULT_DATA_DIR = './data/'
_DEFAULT_SAVE_DIR = './output/'
_DEFAULT_CROP_POLICY = False
_INTENSITY_THRESHOLD = 128
_MIN_CIRCULARITY, _MAX_CIRCULARITY = 0.8, 1.2
_MIN_PERIMETER = 50


def process_data_single(img_path,
                 output_img_path,
                 crop=_DEFAULT_CROP_POLICY,
                 threshold=None):

    image = cv2.imread(str(img_path), 1)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    area, feeding_structures = detect_hyphae_area(image, crop=crop, threshold=threshold)
    cv2.imwrite(output_img_path, feeding_structures)
    ## Upload result to S3
    output_img_path_s3 = upload_toS3(output_img_path)
    print(area)
    print(output_img_path_s3)
    return output_img_path_s3, area



def detect_hyphae_area(img, crop=False, threshold=None):
    if crop:
        crop_mask = crop_img(img)
        if crop_mask is not None:
            cv_plot(img, "Cropped Image.")
    h, w = img.shape[:2]
    original_img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 9, 75, 75)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST,
                                                cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [
        contour for contour in contours if valid_contour(contour, thresh)
    ]
    ## print("Kept {} / {} contours.".format(
    ##    len(filtered_contours), len(contours)))
    feeding_structures = img.copy()
    mask = np.zeros(thresh.shape, np.uint8)
    cv2.drawContours(mask, filtered_contours, -1, 255, -1)
    cv2.drawContours(feeding_structures, filtered_contours, -1, (0, 255, 0), 1)
    if crop and crop_mask is not None:
        feeding_structures[crop_mask] = original_img[crop_mask]
    else:
        _zero_border(feeding_structures)
        _zero_border(mask)

    area = 1 - (np.count_nonzero(mask) / mask.size)
    display_img = np.hstack([original_img, feeding_structures])
    ## cv_plot(display_img, "Image with contours")
    return area, display_img


def _zero_border(img):
    img[0, :] = 0
    img[-1, :] = 0
    img[:, 0] = 0
    img[:, -1] = 0
    return img


def valid_contour(cnt, thresh):
    perimeter = cv2.arcLength(cnt, True)
    if perimeter < _MIN_PERIMETER:
        return False

    area = cv2.contourArea(cnt)
    circularity = 4 * math.pi * (area / (perimeter * perimeter))
    mask = np.zeros(thresh.shape, np.uint8)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(mask, center, radius, 255, cv2.FILLED)
    pixelpoints = np.nonzero(mask)
    pixel_intensities = thresh[pixelpoints].flatten()
    pixel_intensities.sort()
    pixel_intensities = pixel_intensities[::-1]
    median_intensity = pixel_intensities[int(len(pixel_intensities) * 0.50)]
    mean_intensity = pixel_intensities.mean()
    if median_intensity < _INTENSITY_THRESHOLD:
        return False
    return True


def crop_img(img):
    h, w = img.shape[:2]
    pts = get_pts(img)
    plt.close('all')
    if len(pts) < 1:
        return None
    mask = np.zeros((h, w))
    cv2.fillPoly(mask, [pts], color=1)
    cords = np.where(mask != 1)
    img[cords] = 0
    return cords


def get_pts(img, tout=-1, bgr=True):
    # Set ginput to retrieve clicks
    if bgr:
        img = img[..., ::-1]

    plt.imshow(img, cmap='gray')
    pts = np.array(plt.ginput(0, timeout=tout)).astype(int)
    plt.show()
    return pts


def cv_plot(img, name, disp_time=1000, window_height=500, window_width=500):
    # Create cv2 window
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, window_height, window_width)

    # Show the image
    cv2.imshow(name, img)
    cv2.waitKey(disp_time)
    cv2.destroyAllWindows()


_ACCEPTABLE_NON_ALPHANUM = ('.', '_', '-', '/')
def _sanitize_name(name):
    return "".join([
        c for c in name
        if c.isalpha() or c.isdigit() or c in _ACCEPTABLE_NON_ALPHANUM
    ]).rstrip()


if __name__ == "__main__":
    filename = sys.argv[1] 
    save_location = sys.argv[1] + '.jpg'
    
    process_data_single(filename, save_location)
