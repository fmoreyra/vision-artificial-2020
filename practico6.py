import numpy as np
import cv2

def translate(image, x, y):
    (h, w) = (image.shape[0], image.shape[1])

    matrix = np.float32([
        [1, 0, x],
        [0, 1, y]
    ])

    return cv2.warpAffine(image, matrix, (w, h))

def rotate(image, angle, center=None, scale=1.0):
    (h, w) = image.shape[:2]

    if center is None:
        center = (w/2, h/2)
    
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    print(matrix)
    print()

    return cv2.warpAffine(image, matrix, (w, h))

def rotate_and_translate(image, angle, tx, ty, center=None):
    angle_in_radians= angle * np.pi / 180
    (h, w) = image.shape[:2]
    scale = 1

    # Another way to calculate matrix, overriding the result of getRotationMatrix2D
    # if center is None:
    #     center = (w/2, h/2)
    # matrix = cv2.getRotationMatrix2D(center, angle, scale)
    # final_matrix = np.float32([
    #     [matrix[0][0], matrix[0][1], scale * tx],
    #     [matrix[1][0], matrix[1][1], scale * ty]
    # ])

    final_matrix = np.float32([
        [scale * np.cos(angle_in_radians), scale * np.sin(angle_in_radians), scale * tx],
        [scale * -np.sin(angle_in_radians), scale * np.cos(angle_in_radians), scale * ty]
    ])
    
    
    print(final_matrix)

    return cv2.warpAffine(image, final_matrix, (w, h))



cv2.imwrite('common/resultadoTP6.png',rotate_and_translate(cv2.imread('common/hoja.png', 0), 45, 120, 120))
# cv2.imwrite('common/resultadoTP6.png',translate(cv2.imread('common/hoja.png', 0), 50, 100))
# cv2.imwrite('common/resultadoTP6.png',rotate(cv2.imread('common/hoja.png', 0), 50))