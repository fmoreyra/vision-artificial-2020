import cv2
import sys

if(len(sys.argv) > 1):
    filename = sys.argv[1]
else:
    print('pass a filename as first argument')
    sys.exit(1)

cap = cv2.VideoCapture(filename)

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    if((cv2.waitKey(cv2.CAP_PROP_FPS)&0xFF) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()