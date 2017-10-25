# USAGE
import cv2
from skimage.filters import threshold_adaptive

from imagelib.pyimagesearch import imutils
from pyimagesearch.transform import four_point_transform


class CamImageScanner:
    def __init__(self, imagePath, outputPath):
        self.imagePath = imagePath
        self.outputPath = outputPath

    def processImage(self):
        image = cv2.imread(self.imagePath)
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)
        print "STEP 1: Edge Detection"
        # convert the image to grayscale, blur it, and find edges
        # in the image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        print "STEP 2: Find contours of paper"
        # find the contours in the edged image, keeping only the
        # largest ones, and initialize the screen contour
        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect

        # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        # warped = threshold_adaptive(warped, 251, offset=10)
        # warped = warped.astype("uint8") * 255

        cv2.imwrite(self.outputPath, warped)
        print "Finished"
        return self.outputPath


# # run the app.
if __name__ == "__main__":
   x = CamImageScanner('./xxx.jpg', './xxxout.jpg')
   x.processImage()