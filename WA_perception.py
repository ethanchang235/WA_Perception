import cv2
import numpy as np

def detect_path_boundaries(image_path):
    """
    Detects path boundaries defined by orange cones in an image and draws boundary lines.

    Args:
        image_path (str): Path to the input image file.
    """
    # 1. Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Image not found at {image_path}")
        return

    original_image = image.copy()

    # 2. Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 3. **ITERATION 4 - FURTHER ADJUSTED** HSV COLOR RANGE AND MORPHOLOGY - **RUN AND CHECK OUTPUT**
    #    Wider Hue range, wider Value range, slightly smaller opening kernel, increased min_contour_area
    lower_orange = np.array([0, 160, 80])    # Adjusted lower bound -  Wider Hue (starts at 0), Value lowered further
    upper_orange = np.array([25, 255, 255])   # Adjusted upper bound - Hue range remains similar, Value range maxed
    # Note: Hue range now from 0 to 25, covering more of the orange spectrum

    # 4. Create a mask to isolate orange regions (cones)
    mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    # 5. Apply morphological operations to clean up the mask - **SMALLER OPENING KERNEL**
    kernel_opening = np.ones((3, 3), np.uint8) # Smaller kernel for opening (3x3 instead of 5x5)
    kernel_closing = np.ones((5, 5), np.uint8) # Kernel for closing remains 5x5
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_opening) # Use smaller kernel for opening
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_closing)

    # 6. Find contours of the cones in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cone_centers = []
    min_contour_area = 50 # **INCREASED min_contour_area** - to filter more noise

    # 7. Calculate the centroid of each significant cone contour
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                cone_centers.append((center_x, center_y))

    # 8. Separate cone centers into left and right sides
    if len(cone_centers) >= 2:
        cone_centers.sort(key=lambda x: x[0])
        num_cones = len(cone_centers)
        left_cones = cone_centers[:num_cones//2]
        right_cones = cone_centers[num_cones//2:]

        sides = []
        if len(left_cones) > 0:
            sides.append(left_cones)
        if len(right_cones) > 0:
            sides.append(right_cones)

        line_color = (0, 0, 255)

        for cone_set in sides:
            if len(cone_set) >= 2:
                x_coords, y_coords = zip(*cone_set)

                # 9. Fit a straight line
                coefficients = np.polyfit(x_coords, y_coords, 1)
                slope, intercept = coefficients

                # 10. Extend lines to the top and bottom of the image
                img_height, img_width, _ = original_image.shape
                y_start = int(slope * 0 + intercept)
                y_end = int(slope * img_width + intercept)

                y_start = max(0, min(img_height - 1, y_start))
                y_end = max(0, min(img_height - 1, y_end))

                # 11. Draw the extended boundary lines
                start_point = (0, y_start)
                end_point = (img_width, y_end)
                cv2.line(original_image, start_point, end_point, line_color, 2)

    # 12. Save the result as answer.png
    cv2.imwrite("answer.png", original_image)
    print("Path boundaries detected and saved as answer.png.")

if __name__ == "__main__":
    detect_path_boundaries("red.png")
