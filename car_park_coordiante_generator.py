import cv2
from src.coordinate_denoter import CoordinateDenoter
from src.utils import IMAGE_PATH, RECT_WIDTH, RECT_HEIGHT

def demostration():
        
    # creating the Coordinate_generator instance for extracting the car park coordinates
    coordinate_generator=CoordinateDenoter()

    # reading and initialing the coordinates 
    coordinate_generator.read_positions()

    # serving the GUI window until user terminates it
    while True:
        
        # refreshing the image
        image =cv2.imread(IMAGE_PATH)

        # drawing the current car park coordinates
        for pos in coordinate_generator.car_park_positions: 
            
            # defning the boundaries
            start = pos
            end = (pos[0]+RECT_WIDTH, pos[1]+RECT_HEIGHT)

            # drawing the rectangle into the image
            cv2.rectangle(image,start,end,(0,0,255),2)
        
        cv2.imshow("Image",image)

        # linking the mouse callback
        cv2.setMouseCallback("Image",coordinate_generator.mouseClick)

        # exit condition
        if cv2.waitKey(1) == ord("q"):
            break

    # re-allocating the sources
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demostration()