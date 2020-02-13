import os
import Comparison
import cv2
from flask import Flask, request, render_template, url_for, redirect, Response
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class VideoCamera(object):
    def __init__(self, filename):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        self.video = cv2.VideoCapture(filename)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if success is True:
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()


app = Flask(__name__)

current_dir = os.path.dirname(__file__);
uploaded_file_name = None
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cropped/start_from/<int:start_from>/end_at/<int:end_at>')
def index_cropped(start_from, end_at):
    ffmpeg_extract_subclip(current_dir+'/videos/my_upload_video.mp4', start_from, end_at,
                           targetname=current_dir+"/videos/cropped.mp4")
    return render_template('cropped_index.html')


@app.route('/duplicates_removed')
def index_duplicates_removed():
    return render_template('duplicates_removed.html')


@app.route('/file_upload')
def file_upload_page():
    return render_template('file_upload_form.html')


@app.route("/upload_video", methods=['POST'])
def handleFileUpload():
    if 'video' in request.files:
        video_file = request.files['video']
        if video_file.filename != '':
            video_file.save(
                os.path.join(os.path.join(os.path.dirname(__file__), 'videos'),
                             "my_upload_video."+video_file.filename.split('.')[1]))
            Comparison.remove_duplicates(
                os.path.join(os.path.join(os.path.dirname(__file__), 'videos'),
                             "my_upload_video."+video_file.filename.split('.')[1]) ,current_dir+'/videos')

    return redirect(url_for('index'))


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/cropped_feed')
def cropped_feed():
    return Response(gen(VideoCamera(current_dir+'/videos/cropped.mp4')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/duplicates_removed_feed')
def duplicates_removed_feed():
    return Response(gen(VideoCamera(current_dir+'/videos/project.avi')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(current_dir+"/videos/my_upload_video.mp4")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', debug=False)
