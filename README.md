# Path Boundary Detection
## Overview
Attempts to detect boundaries of a straight path defined by cones. The algorithm processes an input image, detects cone boundaries using color segmentation and contour analysis, and outputs an image with boundary lines drawn.

## Output
The processed image with detected boundaries is saved as `answer.png`.

## Methodology
### Image Loading:
The input image is read using OpenCV.

### Color Space Conversion:
The image is converted from BGR to HSV color space, which helps in better segmentation of colors based on hue, saturation, and value.

### Cone Detection:
A binary mask is created to identify cones based on a specific HSV color range designed to capture orange cones. The HSV range used is:
*   **Lower bound (HSV):** `[0, 160, 80]`
*   **Upper bound (HSV):** `[25, 255, 255]`

### Morphological Operations:
Morphological operations are applied to the binary mask to reduce noise and refine the shape of detected cone regions:
*   **Opening**:  Removes small noise pixels using a 3x3 kernel.
*   **Closing**: Fills small holes in the detected cone regions using a 5x5 kernel.

### Contour Detection:
Contours of the detected cones in the processed mask are found. Small contours, specifically those with an area less than 50 pixels, are filtered out to minimize noise and focus on significant cone detections.

### Boundary Line Fitting:
The centers of detected cones (centroids of contours) are computed. If at least two cone centers are detected, they are separated into left and right groups based on their x-coordinates.  Straight lines are then fitted to the sets of left and right cone centers using linear regression. These lines are extended to the full image width to represent path boundaries.

### Visualization:
The original image is annotated by drawing red lines representing the fitted boundary lines. This annotated image is then saved.

## What Was Attempted That Did Not Work
### Color Range Tuning:
Initially, defining the precise HSV color range for accurate cone detection was challenging. Iterative adjustments and testing were necessary to refine the color range to effectively capture the orange cones while minimizing the detection of non-cone orange elements in the scene.  Earlier iterations likely used less refined ranges, leading to either incomplete cone detection or excessive noise in the mask.

### Contour Area Filtering:
Setting an appropriate threshold for contour area filtering is crucial.  Setting the `min_contour_area` too low resulted in the algorithm capturing noise and very small, irrelevant contours. While increasing the threshold to `50` helped reduce noise, it also risks missing smaller or more distant cones.  Finding a balance is key.

### Line Fitting with Insufficient Cones:
The line fitting step requires a sufficient number of detected cones to produce meaningful path boundaries. In scenarios where cone detection is poor, or fewer than two cones are detected on either side of the path, the line fitting process might not produce reliable results, or might not execute at all if fewer than two cones are found in total. The code was designed to handle cases with fewer cones gracefully by only attempting line fitting if at least two cones are detected.

## Libraries Used
- **OpenCV (cv2)**: The primary library for image processing tasks. It is used for reading images, converting color spaces, creating masks, applying morphological operations, detecting contours, calculating contour moments, drawing lines, and saving images.
- **NumPy (np)**: Used for numerical operations and handling arrays, particularly for defining color ranges, creating kernels for morphological operations, and performing polynomial (line) fitting.

## Requirements
Make sure you have the following Python packages installed:
```bash
pip install opencv-python numpy
