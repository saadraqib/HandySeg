import cv2
import numpy as np
def gray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def convert2binary(gray_scale_img):
    return cv2.threshold(gray_scale_img, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]

def find_pp(binary_img, axis=0):
    return np.sum(binary_img, axis=axis)

def cut_blank_header_footer(img, upside_peaks):

    first_line = upside_peaks[0]
    last_line = upside_peaks[-1]
    if ((first_line - 40) < 0):
        pass
    else:
        point_to_cut = first_line - 40
        img = img[point_to_cut:, :]
        upside_peaks = np.array(upside_peaks) - point_to_cut

    if (last_line + 50 > img.shape[0]):
        pass
    else:
        img = img[:last_line + 50, :]
    return img, upside_peaks

def first_and_last_line(img,seams):
    # converting seams list to numpy array
    seams = np.array(seams)
    # squeezing the array
    seams = seams[:,:,0]
    # adding the first line and the last line intervals into the seams
    first_line_minimum = np.min(seams[0][:])
    last_line_maximum = np.min(seams[-1][:])
    if ((first_line_minimum - 200) >= 0):
        # maximum = np.max(seams[0][:])
        seams = np.insert(seams, 0, np.array([first_line_minimum - 200] * seams.shape[1]), axis=0)
    else:
        seams = np.insert(seams, 0, np.array([0] * seams.shape[1]), axis=0)
    if ((last_line_maximum + 200) <= img.shape[0]):
        seams = np.insert(seams, seams.shape[0], np.array([last_line_maximum + 200] * img.shape[1]), axis=0)
    else:
        seams = np.insert(seams, seams.shape[0], np.array([img.shape[0]] * img.shape[1]), axis=0)

    return seams

def blank_line(difference,cols):
    blank_line = np.array([[[255]*3]*cols]*difference)
    return blank_line

def segmented_lines(img,seams, line_index=0):

    difference = np.max(seams[line_index + 1, :]) - np.min(seams[line_index, :])

    mini = np.min(seams[line_index])
    maximum = np.max(seams[line_index + 1])

    white_line = blank_line(difference, img.shape[1])

    for i in range(img.shape[1]):
        initial_pt = (seams[line_index][i] - mini)
        last_pt = (maximum - mini) - (maximum - seams[line_index + 1][i])
        white_line[initial_pt:last_pt, i] = img[seams[line_index][i]:seams[line_index + 1][i], i]

    return white_line

def mark_horizontal_seam(image, seams, color=0):

    # Mark the seam on the image with a specified color
    marked_image = image.copy()
    for seam in seams:
        for i, j in seam:
            marked_image[i, j] = color

    return marked_image