class WhitespaceSteganography:
    
    # Hides the payload text within the whitespace characters of the cover text file and 
    # writes the encoded text to the output file.
    def hide_text_payload(self, cover_file, payload_file, output_file):
        
        # Read the cover text from the file
        with open(cover_file, 'r', encoding='utf-8') as file:
            cover_text = file.read()

        # Read the payload text from the file
        with open(payload_file, 'r', encoding='utf-8') as file:
            payload_text = file.read()

        # Convert the payload to binary representation
        binary_payload = ''.join(format(ord(char), '08b') for char in payload_text)

        # Check the length of the binary payload
        payload_length = len(binary_payload)
        max_length = len(cover_text) - cover_text.count(' ')  # Maximum available whitespace characters
        if payload_length > max_length:
            raise ValueError(f"Payload length ({payload_length}) exceeds the available whitespace length ({max_length}).")

        # Hide the binary payload within the whitespace characters of the cover text
        encoded_text = ""
        payload_index = 0
        for char in cover_text:
            if char.isspace() and payload_index < payload_length:
                # Replace whitespace characters with non-breaking space characters (U+00A0)
                encoded_text += "\u00A0" if binary_payload[payload_index] == '1' else " "
                payload_index += 1
            else:
                encoded_text += char

        # Write the encoded text to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(encoded_text)


    # Extracts the hidden payload from the encoded file.
    # returns the extracted payload string
    def extract_hidden_payload(self, encoded_file):
        
        # Read the encoded text from the file
        with open(encoded_file, 'r', encoding='utf-8') as file:
            encoded_text = file.read()

        # Extract the hidden payload from the non-breaking space characters (U+00A0)
        binary_payload = ""
        for char in encoded_text:
            if char == '\u00A0':
                binary_payload += '1'
            elif char == ' ':
                binary_payload += '0'

        # Convert the binary payload to bytes
        payload_bytes = bytes(int(binary_payload[i:i+8], 2) for i in range(0, len(binary_payload), 8))

        # Convert the payload bytes to a string
        payload_string = payload_bytes.decode('utf-8')

        # Return the payload string
        return payload_string

if __name__ == "__main__":
    
    # Create an instance of the whitespaceSteganography class
    obj = WhitespaceSteganography()

    # To encode
    obj.hide_text_payload("files/cover.txt", "files/payloadtest.txt", "files/encoded.txt")
    print("Text payload successfully hidden.")

    # To decode
    payload = obj.extract_hidden_payload("files/encoded.txt")
    print("Text payload successfully extracted:", payload)
