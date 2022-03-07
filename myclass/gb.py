import cv2
import base64
#class to handle cropping options
class Cut:
#function to crop image
#Parameters: image to crop, contour, and the image number
     def crop(self,image,imagecrop):
        image = cv2.imread(image)
        crop = image[205:267,519:700]
        cv2.imwrite(imagecrop+'.png', crop)

        with open(imagecrop+".png", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        return my_string.decode('utf-8')