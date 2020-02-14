import cv2
from skimage.measure import compare_ssim


def image_compare(prev_image, current_image):
    grayA = cv2.cvtColor(prev_image, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    return (score)

    # Opens the Video file


def remove_duplicates(file_name, path):
    print(file_name)
    cap = cv2.VideoCapture(file_name)
    # i=0
    frame_previous = cv2.imread('blank.jpg')
    height, width, layers = frame_previous.shape
    size = (width, height)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(path+'/project.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        score = image_compare(frame_previous, frame);
        if score < 0.9:
            # cv2.imwrite('\Trimmed\kang'+str(i)+'.jpg',frame)
            video.write(frame)
            # i+=1
        frame_previous = frame;

    cap.release()
    video.release()
    cv2.destroyAllWindows()
