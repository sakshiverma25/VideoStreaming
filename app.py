import os
import Comparison
import Cropping
import cv2
from flask import Flask, request, render_template, url_for, redirect, Response


# Defining Class VideoCamera for handling the initialization and frame Conversion
class VideoCamera(object):
    def __init__(self, filename):
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
# getting the current path so that Videos are stored at the desired location
current_dir = os.path.dirname(__file__);
uploaded_file_name = None

# For original Video Streaming
@app.route('/')
def index():
    return render_template('index.html')

# For cropped Video Streaming
@app.route('/cropped/start_from/<int:start_from>/end_at/<int:end_at>')
def index_cropped(start_from, end_at):
    Cropping.Crop_Video(current_dir+'/videos/my_upload_video.mp4', start_from, end_at,
                           current_dir+"/videos/cropped.mp4")
    return render_template('cropped_index.html')

# For Video Streaming after removing duplicates frames
@app.route('/duplicates_removed')
def index_duplicates_removed():
    return render_template('duplicates_removed.html')

# For uploading the local video file
@app.route('/file_upload')
def file_upload_page():
    return render_template('file_upload_form.html')

# Post method for video upload
@app.route("/upload_video", methods=['POST'])
def handleFileUpload():
    if 'video' in request.files:
        video_file = request.files['video']
        if video_file.filename != '':
            print(os.path.join(os.path.join(current_dir, 'videos'),
                             "my_upload_video."+video_file.filename.split('.')[1]))
            video_file.save(
                os.path.join(os.path.join(current_dir, 'videos'),
                             "my_upload_video."+video_file.filename.split('.')[1]))
            Comparison.remove_duplicates(
                os.path.join(os.path.join(current_dir, 'videos'),
                             "my_upload_video."+video_file.filename.split('.')[1]) ,current_dir+'/videos')

    return redirect(url_for('index'))

# generator method
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
    return Response(gen(VideoCamera(current_dir+'/videos/project.mp4')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    print(current_dir+"/videos/my_upload_video.mp4")
    return Response(gen(VideoCamera(current_dir+"/videos/my_upload_video.mp4")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
