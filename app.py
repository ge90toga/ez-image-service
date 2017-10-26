from flask import Flask, abort, request, send_from_directory
import shutil
import requests
import json
from imagelib.scan import CamImageScanner
from imagelib.errors.error import ContourNotFoundError, NotA4Error

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
    cam = CamImageScanner(fileNameExt, 'images/processed/' + file)
    try:
        cam.processImage()
    except ContourNotFoundError:
        response = app.response_class(
            response=json.dumps({'err': 'fail to find edge'}),
            status=400,
            mimetype='application/json'
        )
        return response
    except NotA4Error:
        response = app.response_class(
            response=json.dumps({'err': 'image size is not a a4 paper'}),
            status=400,
            mimetype='application/json'
        )
        return response
    try:
        cam.checkAndRotate()
    except:
        response = app.response_class(
            response=json.dumps({'err': 'rotation error'}),
            status=400,
            mimetype='application/json'
        )
        return response
    # delete both images on server after s3 upload
    url = AWS_PUBLIC_DNS + '/images/processed/' + fileNameExt.split("/")[-1]
    response = app.response_class(
        response=json.dumps({'url': url}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/hello')
def hello_world():
    return 'Hello, I am ezswitch image optimiser!'


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()
