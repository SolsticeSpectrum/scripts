# We will use wave package available in native Python installation to read and write .wav audio file
import wave
# read wave audio file
song = wave.open("song.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# The "secret" text message
string='Nice job! Here you have one key as bonus for the effort: 4B36CBB7-9703-426F-8F90-608C58841F85, 25E802A2-6E88-405F-95DB-C6A50E27011C'
# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
# Get the modified bytes
frame_modified = bytes(frame_bytes)

# Write bytes to a new wave audio file
with wave.open('song_embedded.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
