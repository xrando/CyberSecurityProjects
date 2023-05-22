from StegnoImg import imgSteg
import cv2
import tkinter  
from Utilities import read_file_content
steg = imgSteg()

if __name__ == "__main__":
	input_image = "t.PNG"
	output_image = "encoded_image.PNG"
	#secret_data = "test message"
	secret_data_file = "t.txt"
	# encode the data into the image
	encoded_image = steg.encode(img=input_image, message=read_file_content(secret_data_file), bits = 1)
	# save the output image (encoded image)
	cv2.imwrite(output_image, encoded_image)
	# decode the secret data from the image
	decoded_data = steg.decode(output_image, bits = 1)
	print("[+] Decoded data:", decoded_data)