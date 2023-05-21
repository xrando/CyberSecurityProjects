import wave
from pydub import AudioSegment
import os

file_directory = "./files/"

# TODO: 1. Allow user to select bits to shift (0 - 5)
#       2. Accept different types of payload (images)


def convert_audio_to_wav(input_file):
    try:
        # Load audio file
        audio = AudioSegment.from_file(file_directory + input_file)
        # Convert it to WAV format (loseless audio format)
        filename, extension = os.path.splitext(input_file)
        output_file = filename + ".wav"
        audio.export(file_directory + output_file, format="wav")
        return output_file

    except Exception as e:
        raise


def encode(input_file, message):
    print("\nEncoding Starts..")
    try:
        # Check if the file is MP3 or MP4 (lossly audio format)
        if input_file.lower().endswith(".mp3") or input_file.lower().endswith(".mp4"):
            input_file = convert_audio_to_wav(input_file)
            if input_file is None:
                return

        audio = wave.open(file_directory + input_file, mode="rb")

        # Convert the audio to byte array
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # Append dummy data to fill out rest of the bytes.
        # Receiver shall detect and remove these characters.
        message = message + int((len(frame_bytes) - (len(message) * 8 * 8)) / 8) * "#"
        # Convert text to bit array
        bits = list(
            map(int, "".join([bin(ord(i)).lstrip("0b").rjust(8, "0") for i in message]))
        )

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

        file_name, extension = os.path.splitext(input_file)

        output_file = file_name + "_stego.wav"

        # Write bytes to a new wave audio file
        newAudio = wave.open(file_directory + output_file, "wb")
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print("succesfully encoded inside", output_file)

    except Exception as e:
        raise


def decode(output_file):
    print("\nDecoding Starts..")

    try:
        audio = wave.open(file_directory + output_file, mode="rb")
        # Convert audio to byte array
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

        # Extract the LSB of each byte
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        # Convert byte array back to message
        message = "".join(
            chr(int("".join(map(str, extracted[i : i + 8])), 2))
            for i in range(0, len(extracted), 8)
        )

        # Remove the filler characters
        decoded = message.split("###")[0]
        print("Sucessfully decoded: " + decoded)
        audio.close()

    except Exception as e:
        raise


if __name__ == "__main__":
    input_audio = "sample_2.mp4"
    output_audio = "sample_2_stego.wav"
    secret_message = "Spiderman is Peter Parker"

    try:
        encode(input_audio, secret_message)
        decode(output_audio)
    except Exception as e:
        print("Error:", str(e))
