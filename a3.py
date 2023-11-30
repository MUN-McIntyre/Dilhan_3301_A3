import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def thresholding(image):
    # convert to gray imgg and then have boundy threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    return mask

def frontImage(foreground, background, mask):
    # make sure mask has 3 chanels
    mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    # we need the mask to bremd imgs
    foreground_masked = cv2.bitwise_and(foreground, mask_3d)
    background_masked = cv2.bitwise_and(background, cv2.bitwise_not(mask_3d))
    combined = cv2.add(foreground_masked, background_masked)
    return combined

def drawShape(image):
    # draw the pentagon
    points = np.array([[100, 100], [200, 50], [300, 100], [250, 200], [150, 200]], np.int32)
    points = points.reshape((-1, 1, 2))
    cv2.polylines(image, [points], True, (0, 255, 0), 3)
    return image

def selectImage():
    # open file dialog
    file_path = filedialog.askopenfilename()
    return file_path

def on_upload_button_click():
    global photo1_path, photo2_path

    photo1_path = selectImage()
    photo2_path = selectImage()

    if not photo1_path or not photo2_path:
        print("No images selected, please select two images.")
        return
    else:
        processImages()

def processImages():
    # load imags
    photo1 = cv2.imread(photo1_path)
    photo2 = cv2.imread(photo2_path)

    # Apply the functions
    mask = thresholding(photo1)
    result = frontImage(photo1, photo2, mask)
    final_result = drawShape(result)

    # display the output image
    cv2.imwrite('final_artwork.jpg', final_result)
    cv2.imshow('Artwork', final_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    # have the main window
    root = tk.Tk()
    root.title("A3")

    root.geometry("300x300")

    # buttn to upload imags
    upload_button = tk.Button(root, text="Upload Images", command=on_upload_button_click)
    upload_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
