import cv2  
import numpy as np  
#ensure that python version is running on 3.9.13
#source: https://www.thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python
# converting types to binary  
class imgSteg:
    def toBinary(self, data):
        #convert different types of data (string, bytes, NumPy array, integer) to binary format
        if type(data) is str:
            return ''.join([ format(ord(i), "08b") for i in data ])
        elif type(data) is bytes:
            return ''.join([ format(i, "08b") for i in data ])
        elif type(data) is np.ndarray:
            return [ format(i, "08b") for i in data ]
        elif type(data) is int or type(data) is np.uint8:
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")
    #function takes in an image file name, message to be hidden, number of least significant bits to use  
    def encode(self, img, message, bits):
        #load image
        image = cv2.imread(img)
        # calculate maximum number of bytes that can be encoded in the image
        #image height*image width*(3 bytes for rgb channel) // 8 bits 
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("[*] Maximum bytes to encode:", n_bytes)
        #checks if the message size exceeds the maximum capacity
        if len(message) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
        print("[*] Encoding data...")
        #prepares the message for encoding by appending a terminating string
        message += "$t3g0"
        data_index = 0
        #converts message to binary format
        messageBinary = self.toBinary(message)
        # size of data to hide
        data_len = len(messageBinary)
        print("Message data Length: " + str(data_len))
        #iterates over each pixel in the image
        for row in image:
            for pixel in row:
                # convert RGB values to binary format
                r, g, b = self.toBinary(pixel)
                #modifies the least significant bits of the RGB values to encode the message
                data = ""
                for i in range(bits):
                    #pad the encoded bits according to number of bits chosen
                    if data_index < data_len:
                        data += messageBinary[data_index]
                        data_index += 1
                    else:
                        #populate extra space with 0
                        data += "0"
                #modifies the least significant bits of the red 
                #component of the pixel by replacing them with the encoded data bits
                pixel[0] = int(r[:-bits] + data, 2)
                data = ""
                for i in range(bits):
                    #pad the encoded bits according to number of bits chosen
                    if data_index < data_len:
                        data += messageBinary[data_index]
                        data_index += 1
                    else:
                        #populate extra space with 0
                        data += "0"
                #modifies the least significant bits of the green 
                #component of the pixel by replacing them with the encoded data bits
                pixel[1] = int(g[:-bits] + data, 2)
                data = ""
                for i in range(bits):
                    #pad the encoded bits according to number of bits chosen
                    if data_index < data_len:
                        data += messageBinary[data_index]
                        data_index += 1
                    else:
                        #populate extra space with 0
                        data += "0"
                #modifies the least significant bits of the blue 
                #component of the pixel by replacing them with the encoded data bits
                pixel[2] = int(b[:-bits] + data, 2)
                # if data is encoded, break out of the loop
                if data_index >= data_len:
                    break
        print(type(image))
        return image
    #
    #def 
    #function takes in an image file name, number of least significant bits to use  
    def decode(self, img, bits):
        print("[+] Decoding...")
        #load image
        image = cv2.imread(img)
        binary_data = ""
        #iterates over each pixel in the image to combine into binary string
        for row in image:
            for pixel in row:
                #slice and extract least significant bits configured that contains message
                r, g, b = self.toBinary(pixel)
                binary_data += r[-bits:]
                binary_data += g[-bits:]
                binary_data += b[-bits:]
        #splits the string into groups of 8 bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        #converts each group to a character
        decoded_data = ""
        for byte in all_bytes:
            #converts binary to int then int to char based on its ascii value, concatenates the characters to form the decoded message
            decoded_data += chr(int(byte, 2))
            #when terminating string met, break out of loop
            if decoded_data[-5:] == "$t3g0":
                break
        #return decoded message without the terminating string
        return decoded_data[:-5]
