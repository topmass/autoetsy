import cv2
import numpy as np

def find_frame_coordinates(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Apply edge detection with adjusted parameters
    edges = cv2.Canny(thresh, 30, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    frame_contour = None
    max_area = 0
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            # Check if the polygon is a rectangle
            _, _, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.8 < aspect_ratio < 1.2:  # More square-like aspect ratio
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    frame_contour = approx

    if frame_contour is not None:
        x, y, w, h = cv2.boundingRect(frame_contour)
        return (x, y, x+w, y+h)
    else:
        return None

def crop_to_frame(image_path, output_path):
    coordinates = find_frame_coordinates(image_path)
    if coordinates:
        image = cv2.imread(image_path)
        x1, y1, x2, y2 = coordinates
        cropped_image = image[y1:y2, x1:x2]
        cv2.imwrite(output_path, cropped_image)
        print(f"Cropped image saved to {output_path}")
    else:
        print("Frame not found. No image was cropped.")

# Example usage
crop_to_frame('path_to_your_image.jpg', 'cropped_image.jpg')
