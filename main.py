

from HandySeg.line_segmentation import line_segmenation
from HandySeg.word_segmentaiton import WordSegmentation
# from HandySeg.preprocessing import *
import matplotlib.pyplot as plt
import cv2


img = cv2.imread(r"C:\Users\saadr\OneDrive\Desktop\files\projects\Datasets\HW_part_IAM_dataset\000_01.png")

# binary_image = convert2binary(img)
# hpp = find_pp(binary_image, axis=1)
#
line_seg = line_segmenation(img,7, show_seam_paths=True)

line_imgs = line_seg.retrieve_line_imgs()
# for i in range(len(imgs)):
#     plt.imshow(imgs[i],cmap='gray')
#     plt.title(f"img index: {i}")
#     plt.show()

word_seg = WordSegmentation(line_imgs[0],True)
# word_boundary = word_seg.retrieve_word_imgs()
# for i in range(len(word_boundary)):
#     plt.imshow(word_boundary[i],cmap='gray')
#     plt.title(f"img index: {i}")
#     plt.show()



