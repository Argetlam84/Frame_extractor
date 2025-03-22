import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
from utils import get_available_resolutions, extract_frames, get_video_info

def browse_video():
    """Select a video file."""
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
    if file_path:
        video_path.set(file_path)
        update_video_info()

def browse_output_folder():
    """Select the output folder."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path.set(folder_path)

def update_video_info():
    """Display video information in the GUI."""
    video_file = video_path.get()
    if not video_file:
        return

    original_res, available_res, fps, frame_count = get_available_resolutions(video_file)

    if original_res:
        original_res_label.config(text=f"Original Resolution: {original_res[0]}x{original_res[1]}")

    if fps is not None:
        fps_label.config(text=f"FPS: {fps}")

        # Update FPS options
        fps_options = get_fps_options(fps)
        fps_dropdown["values"] = ["Original"] + fps_options
        fps_var.set("Original")  # Default to original FPS

    if frame_count is not None:
        frame_count_label.config(text=f"Total Frame Count: {frame_count}")

    resolution_dropdown["values"] = ["Original"] + available_res
    resolution_var.set("Original")

def get_fps_options(original_fps):
    """Generate FPS options from 1 to the original FPS value."""
    return [str(i) for i in range(1, original_fps + 1)]

def start_extraction():
    """Start the extraction process in a separate thread."""
    extraction_thread = threading.Thread(target=run_extraction)
    extraction_thread.start()

def run_extraction():
    """Perform the frame extraction process."""
    video_file = video_path.get()
    output_folder = output_path.get()
    resolution = resolution_var.get()
    fps = fps_var.get()

    if not video_file or not output_folder:
        messagebox.showerror("Error", "Please select a video file and an output folder!")
        return

    if resolution == "Original":
        resolution = None  # Use the original resolution

    if fps == "Original":
        fps = None  # Use the original FPS
    else:
        fps = int(fps)  # Convert selected FPS to an integer

    progress_bar["value"] = 0
    progress_label.config(text="Progress: 0%")

    success, msg = extract_frames(video_file, output_folder, resolution, fps, update_progress)

    if success:
        progress_label.config(text="Completed!")
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", msg)

def update_progress(percent):
    """Update the progress bar."""
    progress_bar["value"] = percent
    progress_label.config(text=f"Progress: {percent:.2f}%")
    root.update_idletasks()

# GUI Setup
root = tk.Tk()
root.title("Video Frame Extractor")

video_path = tk.StringVar()
output_path = tk.StringVar()
resolution_var = tk.StringVar()
fps_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Video Selection
tk.Button(frame, text="Select Video", command=browse_video).grid(row=0, column=0, columnspan=2, pady=5)

# Video Information
original_res_label = tk.Label(frame, text="Original Resolution: -")
original_res_label.grid(row=1, column=0, columnspan=2, pady=5)

fps_label = tk.Label(frame, text="FPS: -")
fps_label.grid(row=2, column=0, columnspan=2, pady=5)

frame_count_label = tk.Label(frame, text="Total Frame Count: -")
frame_count_label.grid(row=3, column=0, columnspan=2, pady=5)

# Resolution Selection
tk.Label(frame, text="Select Resolution:").grid(row=4, column=0, pady=5)
resolution_dropdown = ttk.Combobox(frame, textvariable=resolution_var, state="readonly")
resolution_dropdown.grid(row=4, column=1, pady=5)

# FPS Selection
tk.Label(frame, text="Select FPS:").grid(row=5, column=0, pady=5)
fps_dropdown = ttk.Combobox(frame, textvariable=fps_var, state="readonly")
fps_dropdown.grid(row=5, column=1, pady=5)

# Output Folder Selection
tk.Button(frame, text="Select Output Folder", command=browse_output_folder).grid(row=6, column=0, columnspan=2, pady=5)

# Start Button
tk.Button(frame, text="Start", command=start_extraction).grid(row=7, column=0, columnspan=2, pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=8, column=0, columnspan=2, pady=5)

# Progress Status
progress_label = tk.Label(frame, text="Progress: 0%")
progress_label.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()
