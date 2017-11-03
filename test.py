from imagelib.scan import CamImageScanner
from imagelib.errors.error import ContourNotFoundError, NotA4Error

cam = CamImageScanner('images/raw/fail1.jpg', 'images/processed/')
# cam.processImage()
