FROM ubuntu

RUN apt-get update
RUN apt-get install python3-pip
RUN apt-get install flask
RUN apt-get install cv2
RUN apt-get install scikit-image
RUN apt-get install ffmpeg-python
ADD app.py /
WORKDIR /
EXPOSE 5000
CMD ["python3","app.py"]