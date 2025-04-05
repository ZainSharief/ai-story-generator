from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy import concatenate_videoclips
from mutagen.mp3 import MP3
import random
import os

from text_to_speech import text_to_speech
from story_generator import story_generator

import time

def get_random_video(folder_path: str) -> VideoFileClip:

    video_list = os.listdir(folder_path) 
    video_list = [x for x in video_list if x.endswith('.mp4')]
    assert len(video_list) > 0, "Error: No videos found in the folder."

    video_path = random.choice(video_list)
    video_path = os.path.join(folder_path, video_path)
    return VideoFileClip(video_path)

def main():

    begin_time = time.time()

    WORDS_PER_FRAME = 4

    prompt = 'Create a scadulous story based on AM I THE ASSHOLE reddit thread. Do not include any additional text, analysis and make it a single paragraph of text. Make the story easy tp follow and use simple words. It cannot be more than 200 words'
    text = story_generator(prompt=prompt)
    text += ' Like and follow for more!' 

    output_audio_path = 'final_audio.mp3'
    timepoints = text_to_speech(text, output_audio_path)

    chunks = text.split(' ')
    chunks = [' '.join(chunks[x:min(x+WORDS_PER_FRAME, len(chunks))]) + ' ' for x in range(0, len(chunks), WORDS_PER_FRAME)]

    video_clip = get_random_video('videos/')
    total_duration = video_clip.duration
    start_time = random.uniform(0, total_duration - 180) # 3 minutes is safe for the video duration

    video_segment_list = []

    for i, text_chunk in enumerate(chunks):

        start_idx = i * WORDS_PER_FRAME
        end_idx = i * WORDS_PER_FRAME + WORDS_PER_FRAME
        end_idx = min(end_idx, len(timepoints) - 1)
        end_time = start_time + (timepoints[end_idx].time_seconds - timepoints[start_idx].time_seconds)

        video_segment = video_clip.subclipped(start_time, end_time)
        segment_duration = video_segment.duration

        # Create the subtitle
        txt_clip = TextClip(
            font="Arial Rounded Bold",
            text=text_chunk, 
            font_size=video_clip.w//10, 
            margin=(10, -int(video_clip.h*(1/8)), 10, 0),
            color = 'white', 
            stroke_color="black", 
            stroke_width=2,     
            method='caption',
            text_align="center",
            size=(video_clip.w-20, video_clip.h - int(video_clip.h*(1/8))),
            duration=segment_duration
        )
        txt_clip = txt_clip.with_position(('center', 'top'))

        # Merge the video and subtitle
        video_segment = CompositeVideoClip([video_segment, txt_clip])  
        video_segment_list.append(video_segment)

        start_time += segment_duration

    # Concatenate the video segments into 1 video and save it
    final_video = concatenate_videoclips(video_segment_list, method="compose")
    final_audio = AudioFileClip('final_audio.mp3')
    final_video = final_video.with_audio(final_audio)
    final_video.write_videofile('final_video.mp4', codec='libx264', audio_codec='mp3')

    # Clean up
    os.remove(output_audio_path)

    print(f'process took {time.time() - begin_time} seconds')

if __name__ == '__main__':
    main()