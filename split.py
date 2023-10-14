import os
import subprocess
import argparse

def split_video(filename, segment_size_mb=100):
    # Calculate segment size in bytes
    segment_size_bytes = segment_size_mb * 1024 * 1024

    # Check the file size
    filesize_bytes = os.path.getsize(filename)
    number_of_segments = int(filesize_bytes / segment_size_bytes) + 1

    # Split the filename to get the base and the extension
    filebase, fileext = os.path.splitext(filename)
    file = os.path.basename(filename)
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(filename), f"{filebase}_segments")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Use ffmpeg to split the video
    for i in range(number_of_segments):
        start_time = i * segment_size_bytes / filesize_bytes
        output_file = f"{output_dir}\\segment_{i + 1}{fileext}"
    
        command = [
            'C:\\Users\\aalis\\Documents\\Code\\ConboyLab\\ffmpeg\\ffmpeg-2023-10-12-git-a7663c9604-essentials_build\\bin\\ffmpeg.exe',
            '-i', filename,
            '-ss', str(start_time),
            '-c', 'copy',
            '-fs', str(segment_size_bytes),
            output_file
        ]

        subprocess.call(command)

    print(f"Video split into {number_of_segments} segments in the directory '{output_dir}'.")
    print(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a video into smaller segments.')
    parser.add_argument('filepath', type=str, help='Path to the video file to be split.')

    args = parser.parse_args()
    split_video(args.filepath)
