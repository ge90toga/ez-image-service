from flask import Flask, abort, request, send_from_directory
import shutil
import requests
import json
from imagelib.scan import CamImageScanner
AWS_PUBLIC_DNS="http://ec2-13-210-137-102.ap-southeast-2.compute.amazonaws.com"
from flask import Response
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
    cam.processImage()
    # delete both images on server after s3 upload
    url = AWS_PUBLIC_DNS+'/images/processed/'+ fileNameExt.split("/")[-1]
    response = app.response_class(
        response=json.dumps({'url':url}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/hello')
def hello_world():
    return 'Hello, I am on heroku!'

# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()
