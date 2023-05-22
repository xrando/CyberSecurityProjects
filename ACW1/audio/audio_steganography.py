import wave
from pydub import AudioSegment
import os
import numpy as np
import math

# TODO: write comments & refactor naming.
#       test out if the payload is too large, and dispaly error messaeg --> done
#       try all the bit ranges, see can decode correctly anot --> done


def roundup(x, base=1):
    return int(math.ceil(x / base)) * base


byte_depth_to_dtype = {1: np.uint8, 2: np.uint16, 4: np.uint32, 8: np.uint64}


def convert_audio_to_wav(input_path, output_path):
    try:
        # Load audio file
        audio = AudioSegment.from_file(input_path)
        # Convert it to WAV format (loseless audio format)
        audio.export(output_path, format="wav")
        return output_path

    except Exception as e:
        raise


def lsb_deinterleave_bytes(carrier, num_lsb, byte_depth=1):
    """
    Deinterleave num_bits bits from the num_lsb LSBs of carrier.

    :param carrier: carrier bytes
    :param num_bits: number of num_bits to retrieve
    :param num_lsb: number of least significant bits to use
    :param byte_depth: byte depth of carrier values
    :return: The deinterleaved bytes
    """
    carrier_dtype = byte_depth_to_dtype[byte_depth]

    # take out the size of the payload first
    header_bits = np.unpackbits(
        np.frombuffer(carrier, dtype=carrier_dtype, count=9 * 8).view(np.uint8)
    ).reshape(9 * 8, 8 * byte_depth)[:, 8 * byte_depth - num_lsb : 8 * byte_depth]

    bytes_to_recover = np.packbits(header_bits).tobytes()[0:4]
    fileExtB = np.packbits(header_bits).tobytes()[5:9]

    fileExt = fileExtB.decode("utf-8")

    num_bits = (int.from_bytes(bytes_to_recover, "little") + 9) * 8

    plen = roundup(num_bits / num_lsb)

    payload_bits = np.unpackbits(
        np.frombuffer(carrier, dtype=carrier_dtype, count=plen).view(np.uint8)
    ).reshape(plen, 8 * byte_depth)[:, 8 * byte_depth - num_lsb : 8 * byte_depth]
    bytes_array = np.packbits(payload_bits).tobytes()[9 : (num_bits) // 8]
    return bytes_array, fileExtB.decode("utf-8", "ignore")


def lsb_interleave_bytes(
    carrier, payload, num_lsb, extPayload, truncate=False, byte_depth=1
):
    """
    Interleave the bytes of payload into the num_lsb LSBs of carrier.

    :param carrier: cover bytes
    :param payload: payload bytes
    :param num_lsb: number of least significant bits to use
    :param truncate: if True, will only return the interleaved part
    :param byte_depth: byte depth of carrier values
    :return: The interleaved bytes
    """

    plen = len(payload)  ## length of payload in bytes
    test_bytes = plen.to_bytes(4, "little")
    test_bytes += str.encode(extPayload)
    padding = "\0" * (5 - len(extPayload))

    test_bytes += str.encode(padding)
    test_bytes += payload

    plen += 9

    payload_bits = np.zeros(shape=(plen, 8), dtype=np.uint8)

    payload_bits[:plen, :] = np.unpackbits(
        np.frombuffer(test_bytes, dtype=np.uint8, count=plen)
    ).reshape(plen, 8)

    bit_height = roundup(plen * 8 / num_lsb)
    payload_bits.resize(bit_height * num_lsb)

    carrier_dtype = byte_depth_to_dtype[byte_depth]
    carrier_bits = np.unpackbits(
        np.frombuffer(carrier, dtype=carrier_dtype, count=bit_height).view(np.uint8)
    ).reshape(bit_height, 8 * byte_depth)

    carrier_bits[:, 8 * byte_depth - num_lsb : 8 * byte_depth] = payload_bits.reshape(
        bit_height, num_lsb
    )

    ret = np.packbits(carrier_bits).tobytes()
    return ret if truncate else ret + carrier[byte_depth * bit_height :]


def encode(audio_path, output_path, payload_path, num_lsb):
    print("\nEncoding Starts..")
    try:
        # Check if the file is MP3 or MP4 (lossly audio format)
        if audio_path.lower().endswith(".mp3") or audio_path.lower().endswith(".mp4"):
            audio_path = convert_audio_to_wav(audio_path, output_path)
            if audio_path is None:
                return

        audio = wave.open(audio_path, mode="rb")

        extPayload = os.path.splitext(payload_path)
        extPayload = extPayload[1]  # the extension

        num_channels = audio.getnchannels()
        num_frames = audio.getnframes()
        sample_width = audio.getsampwidth()
        num_samples = num_frames * num_channels

        # We can hide up to num_lsb bits in each sample of the audio file
        max_bytes_to_hide = (num_samples * num_lsb) // 8
        payload_size = os.stat(payload_path).st_size

        print(f"Using {num_lsb} LSBs, we can hide {max_bytes_to_hide} bytes")

        audio_frames = audio.readframes(num_frames)

        with open(payload_path, "rb") as file:
            payload = file.read()

        if payload_size > max_bytes_to_hide:
            raise ValueError("Input file too large to hide")

        audio_frames = lsb_interleave_bytes(
            audio_frames, payload, num_lsb, extPayload, byte_depth=sample_width
        )

        print(f"{payload_size} bytes hidden")

        # Write bytes to a new wave audio file
        audio_steg = wave.open(output_path, "wb")
        audio_steg.setparams(audio.getparams())
        audio_steg.writeframes(audio_frames)

        audio_steg.close()
        print("succesfully encoded inside", output_path)

    except Exception as e:
        raise


def decode(audio_path, output_path, num_lsb):
    print("\nDecoding Starts..")

    try:
        # Open the audio file that has been encoded
        audio = wave.open(audio_path, mode="rb")

        sample_width = audio.getsampwidth()
        num_frames = audio.getnframes()
        audio_frames = audio.readframes(num_frames)

        data, fileExt = lsb_deinterleave_bytes(
            audio_frames, num_lsb, byte_depth=sample_width
        )

        fileExt = fileExt.rstrip("\x00")

        output_file = open(output_path, "wb+")
        output_file.write(bytes(data))
        output_file.close()

        print("Sucessfully decoded: " + data.decode("utf-8"))

    except Exception as e:
        raise


if __name__ == "__main__":
    file_directory = "./files/"

    input_audio_path = file_directory + "sample_3.wav"
    output_audio_path = file_directory + "encode_stego.wav"
    payload_path = file_directory + "payload_large.txt"

    try:
        num_lbs = 67
        while num_lbs > 6:
            num_lbs = int(input("Please enter the number of LBS to replace (1-6): "))
            if num_lbs <= 6:
                encode(input_audio_path, output_audio_path, payload_path, num_lbs)
                decode(output_audio_path, payload_path, num_lbs)
    except Exception as e:
        print("Error:", str(e))
