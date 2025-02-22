from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy import concatenate_videoclips
from mutagen.mp3 import MP3
import random
import os

from text_to_speech import text_to_speech
from story_generator import story_generator

def get_random_video(folder_path: str) -> VideoFileClip:
    video_list = os.listdir(folder_path)
    video_path = random.choice(video_list)
    video_path = os.path.join(folder_path, video_path)
    return VideoFileClip(video_path)

def estimate_timing(text_chunk: str, start_time: float, characters_per_second: float) -> float:

    # Pretty awful estimate right now, TODO: Improve this
    duration = len(text_chunk) / characters_per_second
    end_time = start_time + duration

    return end_time

def main():

    prompt = 'Create a scadulous story based on AM I THE ASSHOLE reddit thread. Do not include any additional text, analysis and make it a single paragraph of text. Make the story easy tp follow and use simple words. It cannot be more than 200 words'
    text = story_generator(prompt=prompt)
    text += ' Like and follow for more!' 

    output_audio = 'final_audio.mp3'
    text_to_speech(text, output_audio)

    audio = MP3(output_audio)
    characters_per_secomd = len(text) / audio.info.length

    # Split the text into chunks of 4 words, edge cases handled
    text = text.split(' ')
    chunks = [' '.join(text[x:min(x+4, len(text))]) + ' ' for x in range(0, len(text), 4)]

    video_clip = get_random_video('videos/')
    total_duration = video_clip.duration
    start_time = random.uniform(0, total_duration - 180) # 3 minutes is safe for the video duration

    video_segment_list = []

    for text_chunk in chunks:

        end_time = estimate_timing(text_chunk, start_time, characters_per_secomd)

        video_segment = video_clip.subclipped(start_time, end_time)
        segment_duration = video_segment.duration

        # Create the subtitle, text is being cropped for some reason, TODO: Fix this
        txt_clip = TextClip(
            font="Arial Rounded Bold",
            text=text_chunk, 
            font_size=45, 
            margin=(10, video_clip.h*(1/8), 10, 0),
            color = 'white', 
            stroke_color="black", 
            stroke_width=2,     
            method='caption',
            text_align="center",
            size=(video_clip.w, None),
            duration=segment_duration
        )   

        # Merge the video and subtitle
        video_segment = CompositeVideoClip([video_segment, txt_clip])  
        video_segment_list.append(video_segment)

        start_time = end_time

    # Concatenate the video segments into 1 video and save it
    final_video = concatenate_videoclips(video_segment_list, method="compose")
    final_audio = AudioFileClip('final_audio.mp3')
    final_video = final_video.with_audio(final_audio)
    final_video.write_videofile('final_video.mp4', codec='libx264', audio_codec='mp3')

    # Clean up
    os.remove(output_audio)

if __name__ == '__main__':
    main()