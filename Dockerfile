FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install Flask
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip3 install opencv-python==4.2.0.32
RUN pip3 install scikit-image==0.15

RUN mkdir /app

COPY app.py /app
COPY blank.jpg /app
COPY Comparison.py /app
COPY Cropping.py /app
COPY templates /app/templates
COPY videos /app/videos
RUN chmod -R 740 /app/*

WORKDIR /app
EXPOSE 5000
CMD ["python3","app.py"]