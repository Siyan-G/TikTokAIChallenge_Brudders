import yt_dlp
import subprocess
import os

def download_video(url, output_name=None):
    
    video_id = output_name if output_name else url.split("/shorts/")[-1].strip()

    os.makedirs("data/temp", exist_ok=True)
    os.makedirs("data/video", exist_ok=True)
    os.makedirs("data/audio", exist_ok=True)
    
    if(os.path.exists(f"data/video/{video_id}.mp4") and os.path.exists(f"data/audio/{video_id}.m4a")):
        print(f"Video and audio already exist for {video_id}")
        return

    # Download video and audio using yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': f'data/temp/{video_id}.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Video downloaded successfully: {video_id}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return
    
    # Process Video (Scale to 720p)
    extract_and_scale_video(f"data/temp/{video_id}.mp4")
    
    # Process Audio (Extract audio only)
    extract_audio(f"data/temp/{video_id}.mp4")
    
    # Clean up temporary files
    os.remove(f"data/temp/{video_id}.mp4")
    os.rmdir("data/temp/")
    print(f"Temporary file removed: data/temp/{video_id}.mp4")

def extract_and_scale_video(path):
    os.makedirs("data/video", exist_ok=True)
    video_id = os.path.basename(path).replace(".mp4", "")
    output_video_path = f"data/video/{video_id}.mp4"
    
    # Use ffmpeg to reduce the video resolution to 720p (no sound)
    command_video = [
        "ffmpeg",
        "-i", path,
        "-an",  # Disable audio
        "-vf", "scale=720:-1",  # Video filter to scale to 720p
        "-c:v", "libx264",  # Video codec
        "-preset", "fast",  # Encoding preset for faster processing
        output_video_path
    ]

    try:
        subprocess.run(command_video, check=True)
        print(f"Video saved as {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing video (no audio): {e}")
        return

def extract_audio(path):
    os.makedirs("data/audio", exist_ok=True)
    
    video_id = os.path.basename(path).replace(".mp4", "")
    output_audio_path = f"data/audio/{video_id}.m4a"
    
    # Use ffmpeg to extract the audio only
    command_audio = [
        "ffmpeg",
        "-i", path,
        "-vn",  # Disable video
        "-ac", "1",  # Mono audio
        "-ar", "44100",  # Audio sample rate
        "-acodec", "aac",  # Audio codec (AAC)
        "-b:a", "192k",    # Audio bitrate
        output_audio_path
    ]

    try:
        subprocess.run(command_audio, check=True)
        print(f"Audio saved as {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing audio: {e}")
        return

# testing 
video = 'https://www.youtube.com/shorts/7ThWB-5buNM'
video2 = 'https://www.youtube.com/shorts/LRqIUqKWGA0'
video_car_crash = 'https://www.youtube.com/shorts/ZEeqUyOA6v0'

download_video(video, 'ina')
download_video(video2, 'ina2')
download_video(video_car_crash, 'car_crash')
