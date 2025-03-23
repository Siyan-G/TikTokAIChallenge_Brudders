import cv2
import os

def extract_frames(video_path, output_folder, frame_interval=10):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(output_folder, video_name)
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"{video_name}_frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1
        frame_count += 1
    cap.release()
    print(f"Total frames: {frame_count}, Frames saved: {saved_count}")

# extract_frames("data/video/ina.mp4", "data/frames/")
# extract_frames("data/video/ina2.mp4", "data/frames/")
# extract_frames("data/video/car_crash.mp4", "data/frames/")