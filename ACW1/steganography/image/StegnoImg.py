import cv2  
import numpy as np  
import imageio
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
        # Read the frames using imageio
        gif_frames = imageio.mimread(img, memtest=False)

        # Convert each frame to an RGB numpy array
        frames = []
        for frame in gif_frames:
            if frame.ndim == 2:
                # Grayscale frame, convert to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            else:
                # RGB frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            frames.append(frame_rgb)

        # Calculate the maximum number of bytes that can be encoded in the frames
        n_bytes = sum(frame.shape[0] * frame.shape[1] * 3 // 8 for frame in frames)
        print("[*] Maximum bytes to encode:", n_bytes)

        # Check if the message size exceeds the maximum capacity
        if len(message) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need a bigger image or less data.")

        print("[*] Encoding data...")
        # Prepare the message for encoding by appending a terminating string
        message += "$t3g0"
        data_index = 0
        # Convert the message to binary format
        messageBinary = self.toBinary(message)
        # Size of data to hide
        data_len = len(messageBinary)
        print("Message data Length:", data_len)

        # Iterate over each frame and each pixel in the frame
        for frame in frames:
            for row in frame:
                for pixel in row:
                    # Convert RGB values to binary format
                    r, g, b = self.toBinary(pixel)

                    # Modify the least significant bits of the RGB values to encode the message
                    data = ""
                    for i in range(bits):
                        # Pad the encoded bits according to the number of bits chosen
                        if data_index < data_len:
                            data += messageBinary[data_index]
                            data_index += 1
                        else:
                            # Populate extra space with 0
                            data += "0"

                    # Modify the least significant bits of the red component of the pixel
                    # by replacing them with the encoded data bits
                    pixel[0] = int(r[:-bits] + data, 2)

                    data = ""
                    for i in range(bits):
                        # Pad the encoded bits according to the number of bits chosen
                        if data_index < data_len:
                            data += messageBinary[data_index]
                            data_index += 1
                        else:
                            # Populate extra space with 0
                            data += "0"

                    # Modify the least significant bits of the green component of the pixel
                    # by replacing them with the encoded data bits
                    pixel[1] = int(g[:-bits] + data, 2)

                    data = ""
                    for i in range(bits):
                        # Pad the encoded bits according to the number of bits chosen
                        if data_index < data_len:
                            data += messageBinary[data_index]
                            data_index += 1
                        else:
                            # Populate extra space with 0
                            data += "0"

                    # Modify the least significant bits of the blue component of the pixel
                    # by replacing them with the encoded data bits
                    pixel[2] = int(b[:-bits] + data, 2)

                    # If data is encoded, break out of the loop
                    if data_index >= data_len:
                        break

        return frames


    #function takes in an image file name, number of least significant bits to use  
    def decode(self, img, bits):
        print("[+] Decoding...")
        # Read the frames using imageio
        gif_frames = imageio.mimread(img, memtest=False)

        binary_data = ""
        # Iterate over each frame and each pixel in the frame
        for frame in gif_frames:
            if frame.ndim == 2:
                # Grayscale frame, convert to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            else:
                # RGB frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

            for row in frame_rgb:
                for pixel in row:
                    # Slice and extract the least significant bits configured that contain the message
                    r, g, b = self.toBinary(pixel)
                    binary_data += r[-bits:]
                    binary_data += g[-bits:]
                    binary_data += b[-bits:]

        # Split the string into groups of 8 bits
        all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]

        # Convert each group to a character
        decoded_data = ""
        for byte in all_bytes:
            # Convert binary to int, then int to char based on its ASCII value
            # Concatenate the characters to form the decoded message
            decoded_data += chr(int(byte, 2))
            # When the terminating string is met, break out of the loop
            if decoded_data[-5:] == "$t3g0":
                break

        # Return the decoded message without the terminating string
        return decoded_data[:-5]
