from StegnoImg import imgSteg
import cv2 
from steganography.Utilities import read_file_content
from tkinter import *
from tkinter import ttk
import imageio

steg = imgSteg()

if __name__ == "__main__":
	input_image = "t.gif"
	#standardize output to be png to prevent loss of metadata due to jpg utilizing lossless compression
	output_image = "encoded_image.gif"
	#secret_data = "test message"
	secret_data_file = "t.docx"
	numOfBit = 6
	# encode the data into the image
	encoded_image = steg.encode(img=input_image, message=read_file_content(secret_data_file), bits = numOfBit)
	# save the output image (encoded image)
	imageio.mimsave(output_image, encoded_image,loop = 0)
	# decode the secret data from the image
	decoded_data = steg.decode(output_image, bits = numOfBit)
	print("[+] Decoded data:", decoded_data)

	root = Tk()
	frm = ttk.Frame(root, width=400, height=300, padding=10)
	frm.pack()
	ttk.Label(frm, text="Hello World!").place(x=20, y=20)
	
	ttk.Button(frm, text="Quit", command=root.destroy).place(x=50, y=50)
	root.mainloop()