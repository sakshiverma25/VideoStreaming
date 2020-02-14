import cv2

def Crop_Video(file_name,start_time,end_time,target):
    # Opens the Video file
    cap= cv2.VideoCapture(file_name)

    frame_previous =cv2.imread('blank.jpg')
    height,width,layers=frame_previous.shape
    size=(width,height)

    fps=int(cap.get(cv2.CAP_PROP_FPS))

    start_frame_index = fps*start_time
    end_frame_index = fps*end_time

    i=0
    video = cv2.VideoWriter(target,cv2.VideoWriter_fourcc(*'MP4V'), fps, size)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        if i in range(start_frame_index,end_frame_index):
            video.write(frame)
        i=i+1;

    cap.release()
    video.release()
    cv2.destroyAllWindows()
