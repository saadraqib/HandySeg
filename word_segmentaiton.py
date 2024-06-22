

from preprocessing import *
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

class WordSegmentation:
    def __init__(self, image):
        self.image = image
        self.binary_image = None
        self.contour_image = None
        self.contours = None
        self.close_img = None
        self.x_bounds = None

    def cut_side_margins(self, smoothing_splines_factor=4):

        threshold = convert2binary(self.image)
        vpp = np.sum(threshold, axis=0)
        smoothed_vpp = gaussian_filter1d(vpp, sigma=smoothing_splines_factor)
        smoothed_vpp[smoothed_vpp < 250] = 0

        start, end = None, None
        length = smoothed_vpp.shape[0]
        for i in range(length - 1):
            if start is None and smoothed_vpp[i] < smoothed_vpp[i + 1]:
                start = i
            if end is None and smoothed_vpp[length - 1 - i] < smoothed_vpp[length - 1 - i - 1]:
                end = length - 1 - i
            if start is not None and end is not None:
                break

        self.image = self.image[:, start:end]
        return self.image

    def compute_contours(self, binary_image):
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contour_image = np.zeros_like(binary_image)
        cv2.drawContours(self.contour_image, contours, -1, 255, 1)
        self.contours = contours
        return self.contour_image, self.contours

    def word_bounds(self):
        contours = list(self.contours)
        x_bounds = []
        for contour in contours:
            if cv2.contourArea(contour) < 30.0:
                continue
            np_contour = np.squeeze(np.array(contour))
            x_bounds.append([np.min(np_contour[:, 0]), np.max(np_contour[:, 0])])
        self.x_bounds = np.sort(x_bounds, axis=0)
        return self.x_bounds

    def cut_blank_top_and_bottom(self, axis=1):
        spaces = []
        for con in self.contours:
            x_arr = np.squeeze(np.array(con))
            if x_arr.shape[0] < 15:
                continue
            try:
                local_min = np.min(x_arr[:, axis])
                local_max = np.max(x_arr[:, axis])
                spaces.extend([local_min, local_max])
            except:
                pass

        spaces = list(set(spaces))
        start = max(min(spaces) - 5, 0)
        end = min(max(spaces) + 5, self.binary_image.shape[0] - 1)
        return start, end

    def close_morphology(self, binary_image):
        length = round(binary_image.shape[1] / 140) * 2
        kernel_standard = length
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_standard, 1))
        close = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=1)
        return close

    def process_image(self):
        self.image = self.cut_side_margins()
        self.binary_image = convert2binary(self.image)
        self.contour_image, self.contours = self.compute_contours(self.binary_image)

        start, end = self.cut_blank_top_and_bottom(axis=1)
        self.binary_image = self.binary_image[start:end, :]
        self.image = self.image[start:end, :]
        self.contour_image = self.contour_image[start:end, :]

        # self.binary_image = convert2binary(self.contour_image)
        self.close_img = self.close_morphology(self.binary_image)
        self.contour_image, self.contours = self.compute_contours(self.close_img)
        self.x_bounds = self.word_bounds()
        return self.x_bounds
