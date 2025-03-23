from transformers import BlipProcessor, BlipForConditionalGeneration
from ultralytics import YOLO
from PIL import Image
from utils.video_extract import extract_frames
import os


def detect_objects(frame_path):
    yolo = YOLO("yolov8n.pt")
    results = yolo(frame_path)
    detect_objects = [yolo.names[int(box.cls)] for box in results[0].boxes]
    return detect_objects

def generate_caption(frame_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    img = Image.open(frame_path).convert("RGB")
    inputs = processor(img, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def create_visual_context(video_path, frame_folder, frame_interval=10):
    extract_frames(video_path, "data/frames/", frame_interval)
    visual_context = {}
    for frame in os.listdir(frame_folder):
        frame_path = os.path.join(frame_folder, frame)
        objects = detect_objects(frame_path)
        caption = generate_caption(frame_path)
        visual_context[frame] = {"objects": objects, "caption": caption, "text": text}
    return visual_context

with open("out.txt", "w") as f:
    print(create_visual_context("data/video/car_crash.mp4", "data/frames/car_crash"), file=f)