import cv2
import numpy as np
import matplotlib.pyplot as plt

MIN_MATCH_COUNT = 10

# 1. Capture images from the same object, but different perspectives
original_img = cv2.imread('common/original.png')
moved_img = cv2.imread('common/moved.png')

# Get grayscale images
original_img_grayscale = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
moved_img_grayscale = cv2.cvtColor(moved_img, cv2.COLOR_BGR2GRAY)

# Initialize SIFT detector and descriptor
# CAUTION!!! This algorithm is not included on CV2 versions bigger than 3.4.2.16 due to license restrictions, as seen on
# https://stackoverflow.com/questions/52305578/sift-cv2-xfeatures2d-sift-create-not-working-even-though-have-contrib-instal
# and related function documentation.
# Tested with opencv-python==3.4.2.16 and python 3.6.9
sift = cv2.xfeatures2d.SIFT_create()

# 2. Get key points and descriptors from both images
original_img_key_points, original_img_descriptors = sift.detectAndCompute(original_img_grayscale, None)
moved_img_key_points, moved_img_descriptors = sift.detectAndCompute(moved_img_grayscale, None)

# 3. Get matches between descriptors
matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(original_img_descriptors, moved_img_descriptors, k=2)

good_matches = []
# 4. Use Lowe criteria to filter between matches
for m, n in matches:
    if m.distance < 0.7*n.distance:
        good_matches.append(m)

# Get homography from filtered matched points
if len(good_matches) > MIN_MATCH_COUNT:
    scr_pts = np.float32([original_img_key_points[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([moved_img_key_points[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(dst_pts, scr_pts, cv2.RANSAC, 5.0)
else:
    print('Not matches found between tested images')
# 5. Apply Homography applied to moved image
img_transformed = cv2.warpPerspective(moved_img, H, (800, 600))

alpha = 0.5
# Mix both images with predefined alpha
mixed_images_result = np.array(img_transformed * alpha + original_img * (1 - alpha), dtype=np.uint8)
img_match = cv2.drawMatchesKnn(
    original_img_grayscale,
    original_img_key_points,
    moved_img,
    moved_img_key_points,
    matches[:10],
    None,
    flags=0
)

cv2.imshow('Mixed images result', mixed_images_result)

plt.imshow(img_match)
plt.show()
cv2.waitKey()
