from StegnoImg import imgSteg
import cv2
import tkinter  

steg = imgSteg()

if __name__ == "__main__":
	input_image = "t.PNG"
	output_image = "encoded_image.PNG"
	secret_data = "test message"
	# encode the data into the image
	encoded_image = steg.encode(img=input_image, message=secret_data, bits = 1)
	# save the output image (encoded image)
	cv2.imwrite(output_image, encoded_image)
	# decode the secret data from the image
	decoded_data = steg.decode(output_image, bits = 1)
	print("[+] Decoded data:", decoded_data)