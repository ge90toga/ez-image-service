# USAGE
import cv2
from skimage.filters import threshold_adaptive
import subprocess
import imutils as imgUitl
from pyimagesearch import imutils
from pyimagesearch.transform import four_point_transform
from errors.error import ContourNotFoundError, NotA4Error
import re

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
        edged = cv2.Canny(gray, 55, 200)

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
            else:
                raise ContourNotFoundError('Cannot find 4 points')

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect

        # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        # warped = threshold_adaptive(warped, 251, offset=10)
        # warped = warped.astype("uint8") * 255
        height, width = warped.shape[:2]
        ratio1 = float(width) / float(height)
        ratio2 = float(height) / float(width)
        if (ratio1 > 0.80 or ratio1 < 0.60) and (ratio2 > 0.80 or ratio2 < 0.60):
            raise NotA4Error('Not a A4 paper: height: ' + str(height) + ' width: ' + str(width))
        cv2.imwrite(self.outputPath, warped)
        print "Finished Transformation"
        return self.outputPath

    def checkAndRotate(self):
        # tesseract image - -psm 0
        # call(['tesseract', 'test.jpg', '-', '-psm', '0'])
        angle = 0
        try:
            x = subprocess.check_output(['tesseract', self.outputPath, '-', '-psm', '0'], stderr=subprocess.STDOUT)
            pattern = r"Orientation in degrees:\s(\d+)"
            matches = re.findall(pattern, x.decode())
            angle = int(matches[0])
            print 'angle: ' + str(angle)
        except Exception as e:
            print "Transformation Angle detection failed"
            print e
        print "start roate"
        if angle != 0:
            img = self.__rotateImage__(self.outputPath, angle)
            cv2.imwrite(self.outputPath, img)
            print "done roate"
        else:
            print "No need to rotate"

    def __rotateImage__(self, imagePath, angle):
        # load the image from disk
        image = cv2.imread(imagePath)
        return imgUitl.rotate_bound(image, angle)

if __name__ == "__main__":
    x = CamImageScanner('test1.jpg', 'test1.jpg')
    x.checkAndRotate()

