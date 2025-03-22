import cv2
import os
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm
from threading import Thread

def extract_frames(video_path, output_folder, interval=1, output_format='jpg', resolution=None, progress_callback=None):
    """Extracts frames from a video at a specified interval and resolution."""
    
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the original frame rate of the video
    frame_interval = int(frame_rate * interval)  # Calculate the interval in frames

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    frame_count = 0
    saved_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video

    # Get the original video resolution
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set the target resolution (if specified)
    if resolution:
        width, height = map(int, resolution.split('x'))
    else:
        width, height = original_width, original_height

    # Supported image formats and their respective quality settings
    valid_formats = {
        "jpg": cv2.IMWRITE_JPEG_QUALITY,
        "png": cv2.IMWRITE_PNG_COMPRESSION,
        "webp": cv2.IMWRITE_WEBP_QUALITY
    }

    # Validate the output format, defaulting to JPG if unsupported
    if output_format not in valid_formats:
        print(f"Unsupported format: {output_format}. Defaulting to jpg.")
        output_format = "jpg"

    print(f"Extracting frames from {video_path} every {interval} seconds at {width}x{height} resolution in {output_format} format...")

    # Progress bar for tracking extraction progress
    with tqdm(total=total_frames, desc="Processing", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Save frame at the specified interval
            if frame_count % frame_interval == 0:
                resized_frame = cv2.resize(frame, (width, height))
                output_path = os.path.join(output_folder, f"frame_{saved_count}.{output_format}")

                # Save the frame in the selected format
                if output_format == "jpg":
                    cv2.imwrite(output_path, resized_frame, [valid_formats[output_format], 95])
                elif output_format == "png":
                    cv2.imwrite(output_path, resized_frame, [valid_formats[output_format], 3])
                elif output_format == "webp":
                    cv2.imwrite(output_path, resized_frame, [valid_formats[output_format], 90])

                saved_count += 1  # Increment the saved frame count

            frame_count += 1
            pbar.update(1)  # Update progress bar
            
            # Call the progress callback function (if provided)
            if progress_callback:
                progress_callback(frame_count, total_frames)

    cap.release()
    cv2.destroyAllWindows()
    print(f"Frames saved in {output_folder}")
