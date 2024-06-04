import cv2

#from ultralytics import RTDETR
from ultralytics import YOLO

# COCO pretrained model
#model: RTDETR = RTDETR('rtdetr-l.pt') too slow on CPU
model: YOLO = YOLO('yolov8n.pt')


def main():
    source = cv2.VideoCapture(0)
    # source = cv2.VideoCapture('video_blue.mp4')

    if (source.isOpened() == False):
        print("Error opening video stream or file")

    win_name = 'Camera'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    '''frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))'''

    frame_rate = source.get(cv2.CAP_PROP_FPS)
    print(f"Webcan frame_rate = {frame_rate}")

    while cv2.waitKey(1) != 27:  # scape
        has_frame, crtFrame = source.read()

        if not has_frame:
            break

        results = model(crtFrame, show=True)
        #cv2.imshow(win_name, crtFrame)

    source.release()
    cv2.destroyWindow(win_name)


if __name__ == '__main__':
    main()
