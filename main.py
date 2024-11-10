import cv2
import numpy as np
from PIL import Image

def create_subtitle_animation(video_path, output_path, target_width=40, fps=10):
    """
    Converts a video into YouTube subtitle format using Unicode block characters
    while maintaining aspect ratio
    
    Parameters:
        video_path: Path to input video
        output_path: Path to save the .srt subtitle file
        target_width: Number of characters wide (height will be calculated)
        fps: Frames per second for the animation
    """
    # Unicode block characters for different shades
    SHADES = '░▒▓█'  # Light to dark blocks
    
    # Open video and get dimensions
    cap = cv2.VideoCapture(video_path)
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate height maintaining aspect ratio
    # Multiply by 0.5 because text characters are typically twice as tall as wide
    target_height = int((target_width * video_height * 0.5) / video_width)
    
    print(f"Original video dimensions: {video_width}x{video_height}")
    print(f"Output dimensions: {target_width}x{target_height} characters")
    
    frame_count = 0
    
    with open(output_path, 'w', encoding='utf-8') as f:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert frame to grayscale and resize
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(gray, (target_width, target_height))
            
            # Convert pixel values to ASCII characters
            ascii_frame = ''
            for row in small:
                for pixel in row:
                    # Map 0-255 to character indices
                    shade_idx = int(pixel / 255 * (len(SHADES) - 1))
                    ascii_frame += SHADES[shade_idx]
                ascii_frame += '\n'
            
            # Calculate timestamps
            start_time = frame_count / fps
            end_time = (frame_count + 1) / fps
            
            # Write subtitle entry
            f.write(f"{frame_count + 1}\n")
            f.write(f"{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n")
            f.write(ascii_frame + "\n\n")
            
            frame_count += 1
            
            if frame_count % 10 == 0:
                print(f"Processed {frame_count} frames...")
    
    cap.release()
    print(f"Done! Created subtitle file with {frame_count} frames")

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Example usage:
if __name__ == "__main__":
    create_subtitle_animation(
        video_path="input.mp4",
        output_path="ne2w.srt",
        target_width=80,
        fps=10
    )