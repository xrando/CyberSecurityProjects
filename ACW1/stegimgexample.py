from steganography.image.StegnoImg import imgSteg
import cv2 
from steganography.Utilities import read_file_content
from tkinter import *
from tkinter import ttk

steg = imgSteg()

if __name__ == "__main__":
	input_image = "test.jpg"
	#standardize output to be png to prevent loss of metadata due to jpg utilizing lossless compression
	output_image = "output/img-1685271658.jpg"
	#secret_data = "test message"
	secret_data_file = "t.docx"
	# encode the data into the image
	encoded_image = steg.encode(img=input_image, message=read_file_content(secret_data_file), bits = 1)
	# save the output image (encoded image)
	cv2.imwrite(output_image, encoded_image)
	# decode the secret data from the image
	decoded_data = steg.decode(output_image, bits = 1)
	print("[+] Decoded data:", decoded_data)