from preprocessing import *
import cv2
from line_segmentation import line_segmenation
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


img = cv2.imread(r"HW_part_IAM_dataset\000_01.png")
gray_scale = gray(img)
binary_image = convert2binary(gray_scale)
hpp = find_pp(binary_image, axis=1)

line_seg = line_segmenation(img, hpp,7, show_seam_paths=True)
seams = line_seg.highlight_seam()
prprcsd_img = line_seg.img
marked_img = mark_horizontal_seam(prprcsd_img,seams)
plt.imshow(marked_img,cmap='gray')
plt.show()
all_seams = first_and_last_line(prprcsd_img,seams)
first_line = segmented_lines(prprcsd_img, all_seams,2)
plt.imshow(first_line,cmap='gray')
plt.show()
