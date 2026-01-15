import cv2 


img = cv2.imread(r"txtused.jpg", cv2.IMREAD_UNCHANGED)
if img is None:
    print("Failed to load image.")
    
