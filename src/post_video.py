from instagrapi import Client
import configparser
import os

def post_video(video_path, caption):
    # Initialize client
    cl = Client()

    config = configparser.ConfigParser()
    config.read("config.ini")

    USERNAME = config['Instagram']['user']
    PASSWORD = config['Instagram']['password']

    # Try loading session
    if os.path.exists("session.json"):
        try:
            cl.load_settings("session.json")
            cl.login(USERNAME, PASSWORD) 

        except Exception as e:
            print(f"An error occurred when loading login: {e}")
            exit(1) 
    else:
        try:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session.json")
            
        except Exception as e:
            print(f"An error occurred during login: {e}")
            exit(1)

    try:
        media = cl.clip_upload(video_path, caption)
        print("Reel posted successfully. Media ID:", media.pk)
    except Exception as e:
        print("Failed to upload reel:", e)

if __name__ == '__main__':

    video_path = "final_video.mp4"
    caption = "Comment your thoughts! #viral #trending #explore #explorepage #foryou #foryoupage #reels #reelsinstagram #instagramreels #reelsvideo #instareels"
        
    post_video(video_path, caption)