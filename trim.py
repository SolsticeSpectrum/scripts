import os
import shutil

input_dir = 'sequence'
output_dir = 'trimmed_sequence'
frames_to_skip = 7

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

frame_number = 0
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith('.png'):
        frame_number += 1
        if frame_number == 1 or (frame_number - 1) % frames_to_skip == 0:
            shutil.copy(os.path.join(input_dir, filename), os.path.join(output_dir, filename))
