import cv2
import pickle
import numpy as np
from src.utils import RECT_HEIGHT, RECT_WIDTH

class ParkClassifier():
        
    def __init__(self, carp_park_positions_path:pickle):
        self.car_park_positions = self._read_positions(carp_park_positions_path)    
    
    def _read_positions(self, car_park_positions_path:pickle)->list:
        
        car_park_positions = None
        try:
            car_park_positions = pickle.load(open(car_park_positions_path, 'rb'))
        except Exception as e:
            print(f"Error: {e}\n It raised while reading the car park positions file.")

        return car_park_positions

    def classify(self, image:np.ndarray, prosessed_image:np.ndarray,threshold:int=1000)->np.ndarray:
        
        #0 for not showing the process steps
        #1 for showing the process steps
        k=0

        if k==1:
            parking_spot_index=1
            copy_image=image.copy()
            cv2.imshow("Copy Image",copy_image)
            cv2.imshow("Processed Image",prosessed_image)
        
        # Finding out the empty and occupied parking spaces and drawing them.
        empty_car_park = 0
        for x, y in self.car_park_positions:
            
            # defining the starting and ending points of the rectangle as cross line
            col_start, col_stop = x, x + RECT_WIDTH
            row_start, row_stop = y, y + RECT_HEIGHT

            # cropping the car park areas form image
            crop=prosessed_image[row_start:row_stop, col_start:x+col_stop]
            
            # counting the number of pixel which below the threshold value reason of the expectation that previous image processing steps
            count=cv2.countNonZero(crop)
            
            # classifying accprding to the threshold value to updating counts and setting drawing params
            empty_car_park, color, thick = [empty_car_park + 1, (0,255,0), 5] if count<threshold else [empty_car_park, (0,0,255), 2]
                
            # drawing the rectangle on the image
            start_point, stop_point = (x,y), (x+RECT_WIDTH, y+RECT_HEIGHT)
            cv2.rectangle(image, start_point, stop_point, color, thick)

            if k==1:
                cv2.rectangle(copy_image, start_point, stop_point, color, thick)
                cv2.putText(copy_image, str(parking_spot_index)+'   '+str(count), (x + 5, y + RECT_HEIGHT - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.rectangle(prosessed_image, start_point, stop_point, (255,255,255), 2)
                print(f"Nr: {parking_spot_index}; start: {start_point}; stop: {stop_point}; collor: {"grean"if color==(0,255,0)else'red'}; count: {count};")
                parking_spot_index+=1
        
        if k==1:
            cv2.imshow("Copy Image with rectangle",copy_image)
            cv2.imshow("Processed Image with rectangle",prosessed_image)
        
        # drawing the legend rectengle where on the tıo left side of the image
        cv2.rectangle(image,(45,30),(250,75),(180,0,180),-1)

        ratio_text = f'Free: {empty_car_park}/{len(self.car_park_positions)}'
        cv2.putText(image,ratio_text,(50,60),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,255,255),2)
        
        return image
        

    def implement_process(self, image:np.ndarray)->np.ndarray:
        #0 for not showing the process steps
        #1 for showing the process steps
        k=0

        # defining the size of kernel matrix param
        kernel_size=np.ones((3,3),np.uint8)

        # gray scaling for reducing colour channel. 
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        
        # gaussian bluring to reduce noise
        blur1=cv2.GaussianBlur(gray, (3,3), 1)
        
        # implementing threashold to get forground object
        Thresholded=cv2.adaptiveThreshold(blur1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        
        # bluring the image to reduce noise and normalize the pixel value gap which is caused by adaptive threshold
        blur2=cv2.medianBlur(Thresholded, 5)
        
        # dilalting for increasing foreground object.
        dilate=cv2.dilate(blur2,kernel_size,iterations=1)

        if k==1:
            cv2.imshow("Gray",gray)
            cv2.imshow("Blur1",blur1)
            cv2.imshow("Thresholded",Thresholded)
            cv2.imshow("Blur2",blur2)
            cv2.imshow("Dilate",dilate)
            
        return dilate