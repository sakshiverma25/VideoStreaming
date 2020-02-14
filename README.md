# VideoStreaming
This project streams local video file to network. Additionally,it also provides the functionality to crop and remove duplicate frames. 

How to build the project:

Pre-requisites:
1.Must have latest docker version installed

How to Build:
1. Open the command prompt parallel to Dockerfile
2. Type 'docker build .' // it will return image name (generated latest)
3. Type 'docker run --rm -p 5000:5000 <image_name>' // sample image name (c6c2939b3352)
4. For checking running process 'docker ps'
5. For kill running container 'docker kill <ContainerID>'

How to Test:
1. Open Browser type 'http(s)://<host_address>:<host_port>'/  // example: http://localhost:5000/

Below API Details:

1. "GET /file_upload HTTP/1.1" 200 (for returning Browse Page)
2. "POST /upload_video HTTP/1.1" 302  (for uploading video from Browser and it will remove duplicate frames and save the video in
                                    separate video file)
3. "GET / HTTP/1.1" 200 (For landing into home page, where video will be streamed into html video tag)
4. "GET /video_feed HTTP/1.1" 200 (For returning stream of stored video)
5. "GET /cropped/start_from/0/end_at/30 HTTP/1.1" 200 (For landing into cropped video page,
                                                        where uploaded video will be cropped and streamed
                                                        depending on the start_from and end_at)
 6. "GET /cropped_feed HTTP/1.1" 200   (For returning stream of cropped video)
 7. "GET /duplicates_removed HTTP/1.1" 200 (For returning the video after removing duplicate frames)

