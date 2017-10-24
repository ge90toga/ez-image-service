import os
from flask import Flask

app = Flask(__name__)
@app.route("/")
def hello():
    text = ''
    try:
        import cv2
        text = 'success'
    except:
        text = 'fail'
        pass
    return 'hello!' + text

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)




# from flask import Flask, abort, request, send_from_directory
# import shutil
# import requests
# import json
# from imagelib.scan import CamImageScanner
#
# app = Flask(__name__)
#
# def download(url):
#     fileNameExt = url.split("/")[-1]
#     fPath = 'images/raw/' + fileNameExt
#     response = requests.get(url, stream=True)
#     with open(fPath, 'wb') as out_file:
#         shutil.copyfileobj(response.raw, out_file)
#     print "downloaded file"
#     return fPath
#
#
# @app.route('/imageOpt', methods=['POST'])
# def imageOpt():
#     if not request.json:
#         abort(400)
#     print "download image from: " + request.json['url']
#     # download image
#     fileNameExt = download(request.json['url'])
#     file = fileNameExt.split("/")[-1]
#     print 'images/processed/' + file
#     cam = CamImageScanner(fileNameExt, 'images/processed/' + file)
#     cam.processImage()
#     # delete both images on server after s3 upload
#     return json.dumps(request.json['url'])
#
#
# # serve static resources:
# @app.route('/images/<path:path>')
# def send_page(path):
#     return send_from_directory('images/processed', path)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, I am on heroku!'
#
# # run the app.
# if __name__ == "__main__":
#     app.debug = True
#     app.run()
