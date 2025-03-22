import cv2
import os

# Standard resolutions dictionary
STANDARD_RESOLUTIONS = {
    "250": (250,250),
    "480p": (854, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "2K": (2560, 1440),
    "4K": (3840, 2160),
}

def get_video_info(video_path):
    """Returns the resolution, FPS, and total frame count of the video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, None, None, None

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    except Exception:
        cap.release()
        return None, None, None, None

    cap.release()
    return (width, height), fps, frame_count

def get_available_resolutions(video_path):
    """Returns the original resolution, available downscaling resolutions, FPS, and frame count."""
    original_res, fps, frame_count = get_video_info(video_path)[:3]
    if not original_res:
        return None, [], None, None

    available_res = [name for name, res in STANDARD_RESOLUTIONS.items() if res[0] <= original_res[0] and res[1] <= original_res[1]]

    return original_res, available_res, fps, frame_count

def extract_frames(video_path, output_folder, resolution=None, fps=None, progress_callback=None):
    """Extracts frames from a video at a specified FPS and resolution."""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False, "Failed to open video!"

        os.makedirs(output_folder, exist_ok=True)

        original_fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_skip = max(1, original_fps // fps) if fps and fps > 0 else 1
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_count = 0
        saved_frames = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                if resolution and resolution in STANDARD_RESOLUTIONS:
                    frame = cv2.resize(frame, STANDARD_RESOLUTIONS[resolution])

                output_path = os.path.join(output_folder, f"frame_{saved_frames:05d}.jpg")
                cv2.imwrite(output_path, frame)
                saved_frames += 1

            frame_count += 1

            if progress_callback:
                progress_callback((frame_count / total_frames) * 100)

        cap.release()
        return True, f"{saved_frames} frames successfully saved!"

    except Exception as e:
        return False, f"Error: {str(e)}"
