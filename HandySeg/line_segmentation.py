import numpy as np
import cv2
from scipy.ndimage import gaussian_filter1d
from HandySeg.preprocessing import *
import matplotlib.pyplot as plt

class line_segmenation:
    def __init__(self,img, smoothing_factor=7, show_seam_paths=False):
        self._img = img
        self._preprocessed_img = None
        self.seams = None

        self._smoothing_factor = smoothing_factor

        self._show_seam_paths = show_seam_paths

        self.__main_function()







    def __find_peaks(self, hpp):
        peaks = []
        stuffed = False
        for i in range(hpp.shape[0] - 1):
            if (hpp[i] > hpp[i + 1] and not stuffed):
                peaks.append(i)
                stuffed = True
            if (hpp[i] < hpp[i + 1]):
                stuffed = False
        return peaks

    def __excluding_missclassified_peaks(self, hpp, peaks):
        length = len(peaks) - 1
        i = -1
        while i < length:
            i += 1
            if (hpp[peaks[i]] < 2500):
                peaks.pop(i)
                length -= 1
                i -= 1

        return peaks

    def __calculate_energy(self,gray_scale):
        # Calculate energy of each pixel using gradient magnitude
        dx = cv2.Sobel(gray_scale, cv2.CV_64F, 1, 0, ksize=5)
        dy = cv2.Sobel(gray_scale, cv2.CV_64F, 0, 1, ksize=5)
        energy_map = np.sqrt(dx ** 2 + dy ** 2)
        return energy_map

    def __find_horizontal_seam(self,energy_map, spots):
        # Find horizontal seam with the lowest energy using dynamic programming
        rows, cols = energy_map.shape

        # Initialize the cost matrix and backtrack matrix
        cost_matrix = np.zeros((rows, cols))
        backtrack_matrix = np.zeros((rows, cols), dtype=np.int64)  # Correct dtype

        # Copy the first column from the energy map to the cost matrix
        cost_matrix[:, 0] = energy_map[:, 0]
        # Calculate cumulative energy for each pixel in the rest of the columns
        for j in range(1, cols):
            for i in range(rows):
                up = max(0, i - 1)
                down = np.min(np.array([rows - 1, i + 1]))  # Renamed 'down' variable
                if (up in spots or down in spots):
                    min_energy_value = cost_matrix[i, j - 1]
                    backtrack_matrix[i, j] = np.argmin(cost_matrix[i, j - 1]) + up

                else:
                    min_energy_value = np.min(
                        np.array([cost_matrix[up, j - 1], cost_matrix[i, j - 1], cost_matrix[down, j - 1]]))
                    backtrack_matrix[i, j] = np.argmin(
                        [cost_matrix[up, j - 1], cost_matrix[i, j - 1], cost_matrix[down, j - 1]]) + up
                cost_matrix[i, j] = energy_map[i, j] + min_energy_value
        return cost_matrix, backtrack_matrix

    def __highlight_seam(self, cost_matrix, backtrack_matrix,spots):
        rows, cols = cost_matrix.shape

        low_energy_indices = []
        for index in range(len(spots) - 1):

            index = index % (len(spots) - 1)
            start_interval = spots[index]
            end_interval = spots[index + 1]
            # cost_matrix[low,-1] = np.max(cost_matrix[start_interval:end_interval,-1])
            lowest_energy_index = np.argmin(cost_matrix[start_interval:end_interval, -1]) + start_interval
            low_energy_indices.append(lowest_energy_index)

        seams = []
        for row in low_energy_indices:
            seam = [(row, cols - 1)]
            for j in range(cols - 1, 0, -1):
                row = backtrack_matrix[row, j]
                seam.append((row, j - 1))
            seams.append(seam[::-1])
        return seams

    def __main_function(self):
        binary_img = self._img.copy()
        binary_img = convert2binary(binary_img)

        hpp = find_pp(binary_img,axis=1)
        smoothed_hpp = gaussian_filter1d(hpp, sigma=self._smoothing_factor)

        peaks = self.__find_peaks(smoothed_hpp)
        spots = self.__excluding_missclassified_peaks(smoothed_hpp, peaks)

        self._preprocessed_img, spots = cut_blank_header_footer(self._img, peaks)
        gray_scale_img = gray(self._preprocessed_img)
        energy_map = self.__calculate_energy(gray_scale_img)
        cost_matrix, backtrack_matrix = self.__find_horizontal_seam(energy_map,spots)
        seams = self.__highlight_seam(cost_matrix, backtrack_matrix,spots)

        if(self._show_seam_paths):
            plt.imshow(mark_horizontal_seam(self._preprocessed_img,seams),cmap='gray')
            plt.show()
        self.seams = first_and_last_line(self._preprocessed_img,seams)

    def retrieve_line_imgs(self):
        line_imgs = []
        for i in range(len(self.seams)-1):
            line_imgs.append(segmented_lines(self._preprocessed_img,self.seams,i))
        return line_imgs






