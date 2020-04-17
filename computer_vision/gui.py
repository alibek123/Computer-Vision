import matplotlib.pyplot as plt
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
apps = []


# Открыть файл
def addApp():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("JPG", "*.jpg"), ("PNG", "*.png"), ("JPEG", "*.jpeg")))
    if filename != "":
        apps.append(filename)
        label1 = tk.Label(frame, text=apps, bg="gray")
        label1.pack()
        drawEdges(filename)
        drawFeatures(filename)
        detect_img_object(filename)


def drawEdges(image):
    img = cv2.imread(image)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("Your Photo", img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.Canny(img, 0, 200)
    cv2.imshow("Edged photo", img)


def drawFeatures(image):
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    minHessian = 400
    #sift = cv2.xfeatures2d.SIFT_create()
    detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)
    keypoints = detector.detect(img)
    img_keypoints = np.empty((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.drawKeypoints(img, keypoints, img_keypoints)
    cv2.imshow("Photo features", img)


def detect_img_object(image):
    img = cv2.imread(image)
    edged = cv2.Canny(img, 10, 250)
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    cv2.imshow("Output", img)

    idx = 0
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 50 and h > 50:
            idx += 1
            new_img = img[y:y + h, x:x + w]
            cv2.imshow(str(idx) + '.png', new_img)
    cv2.waitKey(0)

# Синий экран
canvas = tk.Canvas(root, height=300, width=300, bg="blue")
canvas.pack()
# Белый экран
frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
# Label
label = tk.Label(frame, text="Choose your photo", fg="black")
label.pack()
# Button
openFile = tk.Button(root, text="Open File", fg='white', bg="gray", command=addApp)
openFile.place(relx=0.4, rely=0.8)

root.mainloop()
