import cv2
import moviepy as mp

def video_crop(input_path: str, output_path: str) -> None:

    '''
    Crops the centre of a video to a 16:9 aspect ratio.
    
    input_path: str: Path to the input video.
    output_path: str: Path to save the cropped video.
    '''

    # Open the video
    video = cv2.VideoCapture(input_path)

    assert video.isOpened(), "Error: Could not open video."
    
    # Get video width, height, and frame rate
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate new dimensions for 16:9 crop
    new_width = int(height * 9 / 16)  
    if new_width > width:
        new_height = int(width * 16 / 9)
        new_width = width
    else:
        new_height = height
    
    # Crop the centre of the video
    x_start = (width - new_width) // 2
    y_start = (height - new_height) // 2
    
    # Save the cropped video
    video = mp.VideoFileClip(input_path)
    cropped_video = video.cropped(x1=x_start, y1=y_start, x2=x_start + new_width, y2=y_start + new_height).without_audio()
    cropped_video.write_videofile(output_path, codec='libx264', fps=fps)

if __name__ == '__main__':

    input_path = "videos/Subway surfers 1 hour Gameplay no commentary free to use.mp4"
    output_path = "videos/subway-surfers_background.mp4"

    video_crop(input_path, output_path)