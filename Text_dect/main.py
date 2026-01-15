# import cv2
# import easyocr
# import os

# img = cv2.imread(r"txtused.jpg", cv2.IMREAD_UNCHANGED)

# if img is None:
#     raise FileNotFoundError(f"Image not loaded. Check path: {'txtused.jpg'}")

# reader = easyocr.Reader(['en'], gpu=False)
# result = reader.readtext(img)

# print(result)

import cv2
import easyocr
import matplotlib.pyplot as plt


img_path = r"Mobile_Bicycle.jpg"
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

# instance of easyocr reader
reader = easyocr.Reader(['en'], gpu=True)

text_ = reader.readtext(img)



#Drawing bounding box around text
for t in text_:

    bbox, text, score = t
    cv2.rectangle(img, bbox[0], bbox[2], (0,255,0), 5)
    cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255,0,0),1)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
