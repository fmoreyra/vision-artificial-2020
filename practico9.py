import cv2
import numpy as np

first_point_x, first_point_y = -1, -1
second_point_x, second_point_y = -1, -1
third_point_x, third_point_y = -1, -1
fourth_point_x, fourth_point_y = -1, -1
count = 0


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


background_image = cv2.imread('common/notebook.jpg')
cv2.namedWindow('background image')
cv2.setMouseCallback('background image', draw)

while (True):
    cv2.imshow('background image', background_image)

    if count is 4:
        # replace with width and height
        selected_image_limit_points = np.float32([
            [0, 0],
            [background_image.shape[1], 0],
            [0, background_image.shape[0]],
            [background_image.shape[1], background_image.shape[0]]
        ])
        background_points = np.float32([
            [first_point_x,     first_point_y],
            [second_point_x,    second_point_y],
            [third_point_x,     third_point_y],
            [fourth_point_x,    fourth_point_y]
        ])
        # Obtaining matrix for transformation
        matrix = cv2.getPerspectiveTransform(background_points, selected_image_limit_points)

        # Transformed added image (in color)
        warped_selected_image = cv2.warpPerspective(background_image, matrix, (background_image.shape[1], background_image.shape[0]))

        cv2.imshow('selected image', warped_selected_image)

    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
    elif k == ord('r'):
        cv2.destroyWindow("final image")
        cv2.destroyWindow("background image")
        background_image = cv2.imread('common/notebook.jpg')
        cv2.imshow('background image', background_image)
        cv2.setMouseCallback('background image', draw)
        count = 0

cv2.destroyAllWindows()
