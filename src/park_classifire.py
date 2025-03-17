import cv2
import pickle
import numpy as np

class ParkClassifier():
        
    def __init__(self, carp_park_positions_path:pickle, rect_width:int=None, rect_height:int=None):
        self.car_park_positions = self._read_positions(carp_park_positions_path) 
        self.rect_height = 48 if rect_height is None else rect_height
        self.rect_width = 107 if rect_width is None else rect_width
    
    
    def _read_positions(self, car_park_positions_path:pickle)->list:
        
        car_park_positions = None
        try:
            car_park_positions = pickle.load(open(car_park_positions_path, 'rb'))
        except Exception as e:
            print(f"Error: {e}\n It raised while reading the car park positions file.")

        return car_park_positions

    def classify(self, image:np.ndarray, prosessed_image:np.ndarray,threshold:int=900)->np.ndarray:
        
        # Finding out the empty and occupied parking spaces and drawing them.
        empty_car_park = 0
        for x, y in self.car_park_positions:
            
            # defining the starting and ending points of the rectangle as cross line
            col_start, col_stop = x, x + self.rect_width
            row_start, row_stop = y, y + self.rect_height

            # cropping the car park areas form image
            crop=prosessed_image[row_start:row_stop, col_start:x+col_stop]
            
            # counting the number of pixel which below the threshold value reason of the expectation that previous image processing steps
            count=cv2.countNonZero(crop)
            
            # classifying accprding to the threshold value to updating counts and setting drawing params
            empty_car_park, color, thick = [empty_car_park + 1, (0,255,0), 5] if count<threshold else [empty_car_park, (0,0,255), 2]
                
            # drawing the rectangle on the image
            start_point, stop_point = (x,y), (x+self.rect_width, y+self.rect_height)
            cv2.rectangle(image, start_point, stop_point, color, thick)
        
        
        # drawing the legend rectengle where on the tıo left side of the image
        cv2.rectangle(image,(45,30),(250,75),(180,0,180),-1)

        ratio_text = f'Free: {empty_car_park}/{len(self.car_park_positions)}'
        cv2.putText(image,ratio_text,(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
        
        return image
        

    def implement_process(self, image:np.ndarray)->np.ndarray:
        
        # defining the size of kernel matrix param
        kernel_size=np.ones((3,3),np.uint8)

        # gray scaling for reducing colour channel. 
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        # gaussian bluring to reduce noise
        blur=cv2.GaussianBlur(gray, (3,3), 1)
        
        # implementing threashold to get forground object
        Thresholded=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        
        # bluring the image to reduce noise and normalize the pixel value gap which is caused by adaptive threshold
        blur=cv2.medianBlur(Thresholded, 5)

        # dilalting for increasing foreground object.
        dilate=cv2.dilate(blur,kernel_size,iterations=1)

        return dilate