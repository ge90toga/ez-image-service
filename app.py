from flask import Flask, abort, request, send_from_directory
import shutil
import requests
import json
from imagelib.scan import CamImageScanner
from imagelib.errors.error import ContourNotFoundError, NotABillError

# Change PUBLIC DNS Name
AWS_PUBLIC_DNS = "http://ec2-13-210-137-102.ap-southeast-2.compute.amazonaws.com"
app = Flask(__name__)

def download(url):
    fileNameExt = url.split("/")[-1]
    fPath = 'images/raw/' + fileNameExt
    response = requests.get(url, stream=True)
    with open(fPath, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    print "downloaded file"
    return fPath


@app.route('/api/imageOpt', methods=['POST'])
def imageOpt():
    if not request.json:
        abort(400)
    print "download image from: " + request.json['url']
    # download image
    fileNameExt = download(request.json['url'])
    file = fileNameExt.split("/")[-1]
    print 'images/processed/' + file
    url = AWS_PUBLIC_DNS + '/images/processed/' + fileNameExt.split("/")[-1]
    cam = CamImageScanner(fileNameExt, 'images/processed/')
    try:
        cam.processImage()
    except ContourNotFoundError:
        return createResponse(400, {'err': 'fail to find edge'})
    try:
        cam.checkAndRotate()
        cam.checkAndRotate()
    except:
        return createResponse(400, {'err': 'Orientation Detection Fail, possibly not a bill', 'url': url})
    try:
        cam.validateBill()
    except NotABillError:
        return createResponse(400, {'err': 'not a bill', 'url': url})
    except Exception:
        return createResponse(400, {'err': 'ocr cmd error', 'url': url})
    # delete both images on server after s3 upload
    url = AWS_PUBLIC_DNS + '/images/processed/' + fileNameExt.split("/")[-1]
    return createResponse(201, {'url': url})

@app.route('/api/hello')
def hello_world():
    return 'Hello, I am ezswitch image optimiser!'

def createResponse(statusCode, messageDict):
    return app.response_class(
        response=json.dumps(messageDict),
        status=statusCode,
        mimetype='application/json'
    )
# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()
