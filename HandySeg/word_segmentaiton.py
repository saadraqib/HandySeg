

from HandySeg.preprocessing import *
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

class WordSegmentation:
    def __init__(self, image, highlight_words=False):
        self._image = image
        self._binary_image = None
        self._contour_image = None
        self._contours = None
        self._close_img = None
        self.x_bounds = None
        self._highlight_words = highlight_words

        self.__main_function()

    def __cut_side_margins(self, smoothing_splines_factor=4):

        threshold = convert2binary(self._image)
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

        self._image = self._image[:, start:end]
        return self._image

    def __compute_contours(self, binary_image):
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self._contour_image = np.zeros_like(binary_image)
        cv2.drawContours(self._contour_image, contours, -1, 255, 1)
        self._contours = contours
        return self._contour_image, self._contours

    def __word_bounds(self):
        contours = list(self._contours)
        x_bounds = []
        for contour in contours:
            if cv2.contourArea(contour) < 30.0:
                continue
            np_contour = np.squeeze(np.array(contour))
            x_bounds.append([np.min(np_contour[:, 0]), np.max(np_contour[:, 0])])
        self.x_bounds = np.sort(x_bounds, axis=0)
        return self.x_bounds

    def __cut_blank_top_and_bottom(self, axis=1):
        spaces = []
        for con in self._contours:
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
        end = min(max(spaces) + 5, self._binary_image.shape[0] - 1)
        return start, end

    def __close_morphology(self, binary_image):
        length = round(binary_image.shape[1] / 140) * 2
        kernel_standard = length
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_standard, 1))
        close = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=1)
        return close

    def __main_function(self):
        self._image = self.__cut_side_margins()
        self._binary_image = convert2binary(self._image)
        self._contour_image, self._contours = self.__compute_contours(self._binary_image)

        start, end = self.__cut_blank_top_and_bottom(axis=1)
        self._binary_image = self._binary_image[start:end, :]
        self._image = self._image[start:end, :]
        self._contour_image = self._contour_image[start:end, :]

        self._close_img = self.__close_morphology(self._binary_image)
        self._contour_image, self._contours = self.__compute_contours(self._close_img)
        self.x_bounds = self.__word_bounds()
        if(self._highlight_words):
            self.__draw_rectangle_around_words()

    def __draw_rectangle_around_words(self):
        new_img = self._image.copy()
        for i in range(len(self.x_bounds)):
            start = (self.x_bounds[i,0],5)
            end = (self.x_bounds[i,1],new_img.shape[0]-5)
            cv2.rectangle(new_img,start,end,0,2)
        plt.imshow(new_img,cmap='gray')
        plt.show()

    def retrieve_word_imgs(self):
        word_imgs = []
        for i in range(len(self.x_bounds)):
            word_imgs.append(segmented_words(self._image,self.x_bounds,i))
        return word_imgs
