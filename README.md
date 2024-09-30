# Path Boundary Detection
## Overview
This project implements a perception algorithm to detect the boundaries of a straight path defined by cones using a camera attached to a vehicle. The algorithm processes an input image, detects cone boundaries, and outputs an image with boundary lines drawn.

## Output
The processed image with detected boundaries is saved as answer.png.

## Methodology
### Image Loading: 
The input image is read using OpenCV.

### Color Space Conversion: 
The image is converted from BGR to HSV color space, which helps in better segmentation of colors.

### Cone Detection: 
A binary mask is created to identify cones based on predefined HSV color ranges.

### Contour Detection: 
Contours of the detected cones are found, and small contours are filtered out to avoid noise.

### Boundary Line Fitting: 
The centers of detected cones are computed, and if sufficient cones are found, a line is fitted between them.

### Visualization: 
The original image is annotated with the detected contours and the fitted boundary line, which is then saved.

## What Was Attempted
### Color Range Tuning: 
Tuning the range for specific cone colors based on the input images could improve detection accuracy.

### Contour Area Filtering: 
Setting the contour area threshold too low could result in capturing noise. Increasing this threshold could reduce unwanted detections, but made it harder to detect small cones.

### Line Fitting: 
If there were not enough detected cones, the line fitting step would fail. To address this, the code was designed to only attempt line fitting when at least two cones are detected.

## Libraries Used
- **OpenCV**: The primary library for image processing tasks. It is used for reading images, converting color spaces, creating masks, detecting contours, and drawing shapes.
- **NumPy**: Used for numerical operations and handling arrays, particularly in the polynomial fitting step.

## Requirements
Make sure you have the following Python packages installed:
```bash
pip install opencv-python numpy

### Usage
To run the algorithm, modify the last line in the provided code to point to your input image. For example:

python
Copy code
detect_path_boundaries("answer.png")  # Image path here
Ensure that the specified image file exists in the same directory as the script, or provide the full path to the image.

The processed image will be saved as answer.png in the same directory.
