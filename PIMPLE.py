import argparse
import numpy as np
import imutils
import cv2
import os
from datetime import datetime

# Create a folder to store the images
output_folder = "output_images/"
os.makedirs(output_folder, exist_ok=True)

# Initialize pimple counter
p = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# Load the image
im = cv2.imread(args["image"])

while True:
    # Crop region of interest
    r = cv2.selectROI("Select Region of Interest", im)
    image = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

    # Splitting the image
    chans = cv2.split(image)
    gray = chans[1]

    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(adaptive.copy(), kernel, 2)

    # Find contours in the threshold image
    cnts = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Loop over the contours
    for c in cnts:
        if 20 < cv2.contourArea(c) < 150:
            x, y, w, h = cv2.boundingRect(c)
            roi = image[y:y + h, x:x + w]
            hsr = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            color = cv2.mean(hsr)
            if int(color[0]) < 10 and int(color[1]) > 70 and int(color[2]) > 90:
                (a, b), radius = cv2.minEnclosingCircle(c)
                if int(radius) < 20:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 0)
                    p += 1

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Save the image with a unique filename
    output_filename = f"{output_folder}image_{timestamp}.jpg"
    cv2.imwrite(output_filename, image)

    # Display the image with detected pimples
    cv2.imshow("Image8", image)

    # Print the number of pimples detected
    print("There are {} pimples in the image".format(p))

    # Wait for a key press and break the loop if 'q' is pressed
    key = cv2.waitKey(0)
    if key == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
