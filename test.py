import cv2
from src.park_classifire import ParkClassifier
from src.utils import CAR_PARK_COORDINATES_PATH, IMAGE_PATH


def demostration():

    # creating the classifier  instance which uses basic image processes to classify
    classifier = ParkClassifier(CAR_PARK_COORDINATES_PATH)

    # Implementation of the classy
    image = cv2.imread(IMAGE_PATH)
        
    # prosessing the image to prepare classify
    prosessed_image = classifier.implement_process(image)
        
    # drawing car parks according to its status
    denoted_image = classifier.classify(image, prosessed_image)
        
    # displaying the results
    cv2.imshow("Car Park Image which drawn According to empty or occupied", denoted_image)

    # exit condition
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demostration()
