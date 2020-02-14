import cv2
from skimage.measure import compare_ssim

# This fucnction checks if two images are similar or not
# It first converts them to grayscale, then computes the score
# score= 1,indicates that the images are same
def image_compare(prev_image, current_image):
    grayA = cv2.cvtColor(prev_image, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    return (score)

    # Opens the Video file

# This function creates a new video after removing duplicate frames from the original video
def remove_duplicates(file_name, path):
    print(file_name)
    cap = cv2.VideoCapture(file_name)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    size = (width, height)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_previous = cv2.resize(cv2.imread('blank.jpg'), size, interpolation=cv2.INTER_AREA)
    video = cv2.VideoWriter(path+'/project.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, size)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        score = image_compare(frame_previous, frame);
        if score < 0.9:
            video.write(frame)
        frame_previous = frame;

    cap.release()
    video.release()
    cv2.destroyAllWindows()
