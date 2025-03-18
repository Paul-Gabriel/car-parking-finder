import cv2
from src.park_classifire import ParkClassifier
from src.utils import CAR_PARK_COORDINATES_PATH, VIDEO_PATH


def demostration():

    # creating the classifier  instance which uses basic image processes to classify
    classifier = ParkClassifier(CAR_PARK_COORDINATES_PATH)

    # Implementation of the classy
    cap = cv2.VideoCapture(VIDEO_PATH)
    while True:

        # reading the video frame by frame
        ret, frame = cap.read()

        # check is there a retval
        if not ret:break
        
        # prosessing the frames to prepare classify
        prosessed_frame = classifier.implement_process(frame)
        
        # drawing car parks according to its status 
        denoted_image = classifier.classify(image=frame, prosessed_image = prosessed_frame)
        
        # displaying the results
        cv2.imshow("Car Park Image which drawn According to  empty or occupied", denoted_image)
        
        # exit condition
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        
        if k & 0xFF == ord('s'):
            cv2.imwrite("output.jpg", denoted_image)

    # re-allocating sources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demostration()
