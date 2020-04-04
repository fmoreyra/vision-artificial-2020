import numpy as np
import cv2

def rotate_and_translate_with_scale(image, angle, tx, ty, center=None, scale=1.0):
    angle_in_radians= angle * np.pi / 180
    (h, w) = image.shape[:2]

    if center is None:
        center = (w/2, h/2)
    
    # Another way to calculate matrix, overriding the result of getRotationMatrix2D
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


cv2.imwrite('common/resultadoTP7.png',rotate_and_translate_with_scale(cv2.imread('common/hoja.png', 0), 45, 120, 120, None, 0.75))