import cv2
img = cv2.imread('common/hoja.png', 0)
thr = 200
for indexOfRow, row in enumerate(img) :
    for indexOfCol, col in enumerate(row):
        if (col > thr):
            img[indexOfRow, indexOfCol] = 255
        else:
            img[indexOfRow, indexOfCol] = 0

cv2.imwrite('common/resultado.png',img)
