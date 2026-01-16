import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# -------------------- HAND DETECTOR --------------------
detector = HandDetector(detectionCon=0.8)

# -------------------- DRAG RECT CLASS --------------------
class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = tuple(posCenter)
        self.size = size
        self.isHovered = False

    def update(self, cursor, smooth=0.25):
        cx, cy = self.posCenter
        x, y = cursor

        # Smooth interpolation (LERP)
        cx = int(cx + (x - cx) * smooth)
        cy = int(cy + (y - cy) * smooth)

        self.posCenter = (cx, cy)

# -------------------- RECTANGLES --------------------
rectList = []
for i in range(5):
    rectList.append(DragRect([i * 250 + 150, 150]))

activeRect = None
cursor = (0, 0)

# -------------------- MAIN LOOP --------------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    lmList = []

    if hands:
        lmList = hands[0]['lmList']

    # -------------------- HAND LOGIC --------------------
    if lmList:
        x1, y1, _ = lmList[8]
        x2, y2, _ = lmList[12]
        l, _, _ = detector.findDistance((x1, y1), (x2, y2), img)

        cursor = (x1, y1)

        if l < 40:  # pinch
            if activeRect is None:
                for rect in rectList:
                    cx, cy = rect.posCenter
                    w, h = rect.size
                    if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
                        activeRect = rect
                        break

            if activeRect:
                activeRect.update(cursor)

        else:
            activeRect = None

    # -------------------- DRAW TRANSPARENT RECTANGLES --------------------
    imgNew = np.zeros_like(img, np.uint8)

    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size

        # Hover detection
        rect.isHovered = False
        if lmList:
            if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
                rect.isHovered = True

        # Color logic
        if rect == activeRect:
            color = (0, 255, 0)      # Green = grabbed
        elif rect.isHovered:
            color = (0, 200, 255)    # Yellow = hover
        else:
            color = (255, 0, 0)      # Red = normal

        cv2.rectangle(
            imgNew,
            (cx-w//2, cy-h//2),
            (cx+w//2, cy+h//2),
            color,
            cv2.FILLED
        )

        thickness = 4 if rect == activeRect else 2
        cvzone.cornerRect(
            imgNew,
            (cx-w//2, cy-h//2, w, h),
            l=20,
            t=thickness,
            rt=0
        )

    # -------------------- BLEND --------------------
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Virtual Drag & Drop", out)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
