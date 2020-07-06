from imutils import perspective, contours, grab_contours
from scipy.spatial.distance import euclidean
import numpy as np
import cv2

# Read image and preprocess
original_image = cv2.imread("common/practico10Referencia.png")

original_image_grayscale = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
# https://docs.opencv.org/2.4/doc/tutorials/imgproc/gausian_median_blur_bilateral_filter/gausian_median_blur_bilateral_filter.html
original_image_filtered = cv2.GaussianBlur(original_image_grayscale, (9, 9), 0)

# https://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
original_image_filtered = cv2.Canny(original_image_filtered, 50, 100)
# https://docs.opencv.org/2.4/doc/tutorials/imgproc/erosion_dilatation/erosion_dilatation.html
original_image_filtered = cv2.dilate(original_image_filtered, None, iterations=1)
original_image_filtered = cv2.erode(original_image_filtered, None, iterations=1)

# Find contours https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
contours_from_filtered_image = cv2.findContours(original_image_filtered.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_from_filtered_image = grab_contours(contours_from_filtered_image)

# Sort contours from left to right as leftmost contour is reference object
(contours_from_filtered_image, _) = contours.sort_contours(contours_from_filtered_image)

# Remove contours which are not large enough
largest_contours_from_filtered_image = [contour for contour in contours_from_filtered_image if cv2.contourArea(contour) < 100]

# Draw real contours
cv2.drawContours(original_image, largest_contours_from_filtered_image, -1, (0, 255, 0), 3)

# Reference from red square (3x3 cm)
reference_object = largest_contours_from_filtered_image[0]
# https://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
reference_rect = cv2.minAreaRect(reference_object)
box = cv2.boxPoints(reference_rect)
box = np.array(box, dtype="int")
(tl, tr, br, bl) = perspective.order_points(box)
dist_in_pixel = euclidean(tl, tr)
dist_in_cm = 10
pixel_per_cm = dist_in_pixel / dist_in_cm

for contour in largest_contours_from_filtered_image:
    object = cv2.minAreaRect(contour)
    object_box_points = cv2.boxPoints(object)
    box = np.array(object_box_points, dtype="int")
    (top_left, top_right, bottom_left, bottom_right) = perspective.order_points(box)
    cv2.drawContours(original_image, [box.astype("int")], -1, (0, 0, 255), 2)
    middle_point_horizontal = (top_left[0] + int(abs(top_right[0] - top_left[0]) / 2), top_left[1] + int(abs(top_right[1] - top_left[1]) / 2))
    middle_point_vertical = (top_right[0] + int(abs(top_right[0] - bottom_right[0]) / 2), top_right[1] + int(abs(top_right[1] - bottom_right[1]) / 2))
    width = euclidean(top_left, top_right) / pixel_per_cm
    height = euclidean(top_right, bottom_right) / pixel_per_cm
    cv2.putText(original_image, "{:.1f}cm".format(width), (int(middle_point_horizontal[0] - 15), int(middle_point_horizontal[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
    cv2.putText(original_image, "{:.1f}cm".format(height), (int(middle_point_vertical[0] + 10), int(middle_point_vertical[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

cv2.imshow("Result", original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()