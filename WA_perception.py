import cv2
import numpy as np

# Define a function to detect the path boundaries
def detect_path_boundaries(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # Convert to HSV color space for better color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the color range for cone detection (tuned for orange cones)
    lower_cone_color = np.array([10, 100, 100])  # Example for orange cones
    upper_cone_color = np.array([25, 255, 255])

    # Create a mask for the cones
    mask = cv2.inRange(hsv, lower_cone_color, upper_cone_color)

    # Find contours of the cones
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the coordinates of the detected cones for drawing boundary lines
    cone_centers = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] > 0:  # Ensure the contour area is non-zero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cone_centers.append((cX, cY))

    # If there are at least two cones on each side, fit lines between them
    if len(cone_centers) >= 4:
        # Sort the centers based on their x-coordinate
        cone_centers.sort(key=lambda x: x[0])

        # Split into two sides, assuming cones are roughly in two vertical lines
        left_cones = cone_centers[:len(cone_centers)//2]
        right_cones = cone_centers[len(cone_centers)//2:]

        # Fit a line for each side
        for cone_set, color in [(left_cones, (0, 0, 255)), (right_cones, (0, 0, 255))]:
            x_coords = [pt[0] for pt in cone_set]
            y_coords = [pt[1] for pt in cone_set]

            # Fit a polynomial (degree 1 for a straight line)
            coefficients = np.polyfit(x_coords, y_coords, 1)
            poly_eq = np.poly1d(coefficients)

            # Draw the line on the image from the minimum to maximum x value
            x_min, x_max = min(x_coords), max(x_coords)
            y_min = int(poly_eq(x_min))
            y_max = int(poly_eq(x_max))
            cv2.line(image, (x_min, y_min), (x_max, y_max), color, 2)

    # Save the result
    cv2.imwrite("answer.png", image)
    print("Boundary lines drawn and saved as answer.png.")

# Main execution block
if __name__ == "__main__":
    # Test the function with an image file
    detect_path_boundaries("red.png")
