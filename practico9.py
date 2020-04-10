import cv2
import numpy as np

first_point_x, first_point_y = -1, -1
second_point_x, second_point_y = -1, -1
third_point_x, third_point_y = -1, -1
fourth_point_x, fourth_point_y = -1, -1
count = 0


def get_mask(img, threshold):
    for indexOfRow, row in enumerate(img):
        for indexOfCol, col in enumerate(row):
            if col > threshold:
                img[indexOfRow, indexOfCol] = 255
            else:
                img[indexOfRow, indexOfCol] = 0
    return img


def draw(event, x, y, flags, param):
    global first_point_x, first_point_y, second_point_x, second_point_y, third_point_x, third_point_y, fourth_point_x, \
        fourth_point_y, count
    if event == cv2.EVENT_LBUTTONUP:
        if count == 0:
            first_point_x, first_point_y = x, y
        if count == 1:
            second_point_x, second_point_y = x, y
        if count == 2:
            third_point_x, third_point_y = x, y
        if count == 3:
            fourth_point_x, fourth_point_y = x, y
        count = count + 1
        cv2.circle(background_image, (x, y), 1, (0, 0, 255), -1)


background_image = cv2.imread('common/Lionel_Messi.jpg')
added_image = cv2.imread('common/cristiano_ronaldo.jpeg')
cv2.namedWindow('background image')
cv2.setMouseCallback('background image', draw)

while (True):
    cv2.imshow('background image', background_image)

    if count is 4:
        added_image_limit_points = np.float32([
            [0, 0],
            [added_image.shape[1], 0],
            [added_image.shape[1], added_image.shape[0]],
            [0, added_image.shape[0]]
        ])
        background_points = np.float32([
            [first_point_x,     first_point_y],
            [second_point_x,    second_point_y],
            [third_point_x,     third_point_y],
            [fourth_point_x,    fourth_point_y]
        ])
        # Obtaining matrix for transformation
        matrix = cv2.getPerspectiveTransform(added_image_limit_points, background_points)

        # Transformed added image (in color)
        warped_added_image = cv2.warpPerspective(added_image, matrix, (background_image.shape[1], background_image.shape[0]))

        # Transformed added image (in grayscale, in order to create the mask)
        warped_added_image_to_grayscale = cv2.cvtColor(warped_added_image, cv2.COLOR_BGR2GRAY)

        # Mask and inverted mask of added image (knowing where to replace pixels on background)
        added_image_mask = get_mask(warped_added_image_to_grayscale, cv2.THRESH_BINARY)
        added_image_inverted_mask = cv2.bitwise_not(added_image_mask)

        # Creation of final image
        final_background = cv2.bitwise_and(background_image, background_image, mask=added_image_inverted_mask)
        final_added_image = cv2.bitwise_and(warped_added_image, warped_added_image, mask=added_image_mask)
        final_image = cv2.add(final_background, final_added_image)

        cv2.imshow('final image', final_image)

    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
    elif k == ord('r'):
        cv2.destroyWindow("final image")
        cv2.destroyWindow("background image")
        background_image = cv2.imread('common/Lionel_Messi.jpg')
        cv2.imshow('background image', background_image)
        cv2.setMouseCallback('background image', draw)
        count = 0

cv2.destroyAllWindows()
