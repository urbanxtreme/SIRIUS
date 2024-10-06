import tkinter as tk  # Added import for tkinter
from PIL import Image, ImageTk
import io
import cv2
import pygame
import threading
def display_image(file_path, container):
    try:
        with open(file_path, 'rb') as file:
            image_data = file.read()
            img = Image.open(io.BytesIO(image_data))
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(container, image=img_tk)
            label.image = img_tk  # Keep a reference
            label.pack()
    except Exception as e:
        print(f"Error displaying image: {str(e)}")


def display_video(file_path, container):
    def run_video():
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image)
            label = tk.Label(container, image=img_tk)
            label.image = img_tk
            label.pack()
            container.update()
        cap.release()

    # Run video playback in a separate thread
    video_thread = threading.Thread(target=run_video)
    video_thread.start()

def play_music(file_path):
    if pygame.mixer.get_busy():
        pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error playing music: {str(e)}")

def stop_music():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
