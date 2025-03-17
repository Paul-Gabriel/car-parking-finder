import cv2
import pickle

class CoordinateDenoter():

    def __init__(self, rect_width:int=107, rect_height:int=48, car_park_positions_path:pickle="data/source/CarParkPos"):
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.car_park_positions_path = car_park_positions_path
        self.car_park_positions = list()

    def read_positions(self)->list:
        
        try:
            self.car_park_positions = pickle.load(open(self.car_park_positions_path, 'rb'))
        except Exception as e:
            print(f"Error: {e}\n It raised while reading the car park positions file.")

        return self.car_park_positions

    def mouseClick(self, events:int, x:int, y:int, flags:int, params:int):
                
        # add car park position to the list 
        if events==cv2.EVENT_LBUTTONDOWN:
            self.car_park_positions.append((x,y))
        
        # remove car park corresonding mouse click
        if events==cv2.EVENT_MBUTTONDOWN:

            # finding out end removing the corresponding label.
            for index, pos in enumerate(self.car_park_positions):
                
                # unpacking
                x1,y1=pos
                
                # setting the condition
                is_x_in_range= x1 <= x <= x1+self.rect_width
                is_y_in_range= y1 <= y <= y1+self.rect_height

                # checking the label is in the range
                if is_x_in_range and is_y_in_range:
                    self.car_park_positions.pop(index)

        # writing the label coordinates into the file
        with open(self.car_park_positions_path,'wb') as f:
            pickle.dump(self.car_park_positions,f)
        