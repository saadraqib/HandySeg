

from HandySeg.line_segmentation import line_segmenation
from HandySeg.word_segmentaiton import WordSegmentation
# from HandySeg.preprocessing import *
import matplotlib.pyplot as plt
import cv2

# import the HandySeg "pip install HandySeg"

img = cv2.imread(r"000_01.png")


# Initialize an object of line_segmentation
# smoothed_factor: It can be varied if there are misclassified lines
# show_seam_paths: Return the images with the lowest seam paths between each two lines, which are marked on the image
line_seg = line_segmenation(img, 7, show_seam_paths=True)


# Retrieve the line images
line_imgs = line_seg.retrieve_line_imgs()

# To view the seams
line_seg.seams


# Display each line image
for i in range(len(line_imgs)):
    plt.imshow(line_imgs[i], cmap='gray')
    plt.title(f"img index: {i}")
    plt.show()

# Initialize a WordSegmentation object
word_seg = WordSegmentation(line_imgs[0], True)

# To show the boundaries of each word
word_seg.x_bounds

# Retrieve and display each word image
word_boundary = word_seg.retrieve_word_imgs()
for i in range(len(word_boundary)):
    plt.imshow(word_boundary[i], cmap='gray')
    plt.title(f"img index: {i}")
    plt.show()




