# HandSeg package 

## 1. Line Segmentation from Handwritten Text

### Overview
Seam Carving and Horizontal Projection Profiles (HPP) are used to segment lines of handwritten text from an image. Initially, HPP is used to detect lines, ensuring the seam's path between lines does not shift outside the boundary, maintaining alignment based on low energy.

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/7932fff8-af64-48e7-ac52-8fa9d7865146" alt="Horizontal projection profile of handwritten text image">
  <br>
  <em>Figure A: Horizontal projection profile of handwritten text image</em>
</p>

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/2de9053e-240f-4aec-b7e2-9f05ebae7f5d" alt="Handwritten part of scanned image (from IAM dataset), crossed out lines">
  <br>
  <em>Figure B: Handwritten text image with crossed out lines</em>
</p>

Energy calculation is performed, and an algorithm is applied to find the low path energies between lines, ensuring paths do not extend beyond the identified rows. This maintains the integrity of the seam's path.

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/6e55a065-e9b9-488d-857d-0cd0244e7e7b" alt="Marked the lowest energy paths between each two lines">
  <br>
  <em>Figure C: The lowest path energies between each two lines</em>
</p>

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/4edc3294-0df3-4879-8c61-6f985d7474f8" alt="Segmented handwritten line text">
  <br>
  <em>Figure D: Segmented handwritten line text</em>
</p>

## 2. Word Segmentation from Segmented Lines

### Overview
First, a Close Morphological operation is applied to the segmented line using a kernel size dependent on both the width and length of the segmented line.

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/c696cada-dcc5-40ba-a3a9-272b4aa5d01e" alt="Segmented handwritten text with Closing Morphological operation">
  <br>
  <em>Figure E: The binary image after applying the Closing Morphological operation</em>
</p>

Next, contours of the preprocessed segmented line image are found.

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/614ec2fd-bbe4-4775-8061-7cf2fac1f267" alt="Drawn a rectangle around each word">
  <br>
  <em>Figure F: Drawn a rectangle around each word</em>
</p>

<p align="center">
  <img src="https://github.com/saadraqib/OCR-for-Scanned-Documents/assets/87097921/22f23ec8-2f76-4fbc-8839-d0eadf490c09" alt="Segmented word">
  <br>
  <em>Figure G: Segmented word</em>
</p>

### Limitations

**Line Segmentation:**
- Does not work well on images with objects other than handwritten text.
- Not effective for lines with a large width.

**Word Segmentation:**
- Ineffective for words with excessive space between characters.
- Not suitable for words with minimal space between them.
