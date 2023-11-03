import os
import subprocess
import argparse


def get_length(filename):
    # Assuming ffmpeg and ffprobe are installed and added to the PATH on the macOS system
    result = subprocess.run(['ffprobe', "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)

def split_video(filename, segment_size_mb=25):
    # Calculate segment size in bytes
    segment_size_bytes = segment_size_mb * 1024 * 1024

    # Check the file size
    filesize_bytes = os.path.getsize(filename)
    number_of_segments = int(filesize_bytes / segment_size_bytes) + 1
    total_duration = get_length(filename)

    # Split the filename to get the base and the extension
    filebase, fileext = os.path.splitext(filename)
    file = os.path.basename(filename)
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(filename), f"{filebase}_segments")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Use ffmpeg to split the video
    # Initialize Start Time
    start_time = 0.0
    segment_number = 0
    segment_duration_seconds = (segment_size_bytes / filesize_bytes) * total_duration

    while True:
        output_file = f"{output_dir}/segment_{segment_number}{fileext}"
        command = [
            'ffmpeg',
            '-i', filename,
            '-ss', str(start_time),
            '-c', 'copy',
            '-t', str(segment_duration_seconds),
            output_file
        ]

        if subprocess.call(command) != 0:
            break
        # Check if the file was created and if its size is small, break
        if os.path.exists(output_file) and os.path.getsize(output_file) < 1000:  # Less than 1KB
            os.remove(output_file)
            break
        # Update start_time for the next segment
        start_time += segment_duration_seconds
        segment_number += 1
        print(f"Processing segment {segment_number} from {start_time}s to {start_time + segment_duration_seconds}s")

    print(f"Video split into {number_of_segments} segments in the directory '{output_dir}'.")
    print(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a video into smaller segments.')
    parser.add_argument('filepath', type=str, help='Path to the video file to be split.')

    args = parser.parse_args()
    split_video(args.filepath)