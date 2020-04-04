import cv2
import numpy as np
import copy

drawing = False
end_x, start_x = -1, -1
end_y, start_y = -1, -1
initial_img = cv2.imread('common/hoja.png', 0)
cropped_img = copy.deepcopy(initial_img)
img = copy.deepcopy(initial_img)

def draw(event, x, y, flags, param):
    global drawing, img, end_x, start_x, end_y, start_y, cropped_img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x = x
        start_y = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            cv2.rectangle(img, (start_x, start_y), (x, y), (0, 255, 0), 1)
    elif event == cv2.EVENT_LBUTTONUP:
        img = copy.deepcopy(initial_img)
        drawing = False
        end_x = x
        end_y = y
        cropped_img = img[start_y:end_y, start_x:end_x]
        cv2.rectangle(img, (start_x, start_y), (x, y), (0, 255, 0), 3)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw)

while (1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
    elif(k == ord('g')):
        cv2.imwrite('common/recorte.png', cropped_img)
        break
    elif(k == ord('r')):
        img = copy.deepcopy(initial_img)
        cropped_img = copy.deepcopy(initial_img)


cv2.destroyAllWindows()
