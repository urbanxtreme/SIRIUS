import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame  # Import pygame for audio playback
import os  # Import os to handle file system operations
from database import fetch_media_by_category

class MediaViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('JWST Exploration App')

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set window geometry to full screen size
        self.geometry(f'{screen_width}x{screen_height}+0+0')

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create a Canvas to hold the background image
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)  # Make the canvas expandable

        # Load the background image
        try:
            self.background_image = Image.open("JWST.jpg")
            self.background_image = self.background_image.resize((screen_width, screen_height), Image.LANCZOS)  # Resize to window size
            self.bg_photo = ImageTk.PhotoImage(self.background_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image 'JWST.jpg' not found.")
            self.bg_photo = None

        # Variables to hold media information
        self.current_media_files = []
        self.image_index = 0
        self.slideshow_running = False
        self.animation_speed = 20  # Fixed animation speed
        self.max_image_size = (screen_width - 100, screen_height - 200)
        self.is_animating = False

        # Create and configure style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='black')
        self.style.configure('TButton', background='#3d3d3d', foreground='#ffffff', font=('Arial', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#4a4a4a')])
        self.style.configure('Category.TButton', background='#2c2c2c', foreground='#00ffff', font=('Arial', 11, 'bold'))
        self.style.map('Category.TButton', background=[('active', '#3a3a3a')])

        # Main window divided into two sections: image and controls
        self.paned_window = tk.PanedWindow(self.canvas, orient=tk.VERTICAL, bg='black')
        self.paned_window.place(x=0, y=0, relwidth=1, relheight=1)

        # Create image display frame
        self.image_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.image_frame, stretch="always")

        self.image_label = tk.Label(self.image_frame, bg='black')
        self.image_label.pack(expand=True)

        # Create controls frame
        self.controls_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.controls_frame, stretch="never")

        # Create buttons for categories
        self.create_category_buttons()

        # Navigation buttons frame
        nav_frame = ttk.Frame(self.controls_frame)
        nav_frame.pack(fill=tk.X, pady=10)

        self.prev_button = ttk.Button(nav_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(nav_frame, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.RIGHT, padx=5)

        self.slideshow_button = ttk.Button(nav_frame, text="Start Slideshow", command=self.toggle_slideshow)
        self.slideshow_button.pack(side=tk.BOTTOM, pady=5)

        self.update_button_state()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Map categories to audio folders
        self.category_audio_map = {
            'Galaxies': 'audio/romantic',
            'Nebulas': 'audio/optimistic',
            'Stars': 'audio/romantic',
            'Cosmology': 'audio/anxiety',
            'Exoplanets': 'audio/enjoy',
            'Solar System': 'audio/loneliness',
            'Webb Mission': 'audio/desperate',
        }

    def create_category_buttons(self):
        category_frame = ttk.Frame(self.controls_frame)
        category_frame.pack(fill=tk.X, pady=(0, 20))

        categories = ['Galaxies', 'Nebulas', 'Stars', 'Cosmology', 'Exoplanets', 'Solar System', 'Webb Mission']

        for category in categories:
            btn = ttk.Button(category_frame, text=category, command=lambda c=category: self.display_media(c), style='Category.TButton')
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def display_media(self, category):
        media_files = fetch_media_by_category(category)
        self.current_media_files = [file for file in media_files if file[1] == 'image']  # Only images
        self.image_index = 0
        self.slideshow_running = False
        self.slideshow_button.config(text="Start Slideshow")

        if self.current_media_files:
            self.show_image()
            self.play_audio_for_category(category)  # Play corresponding audio
        else:
            messagebox.showinfo("No Media", f"No media found for category '{category}'.")

    def show_image(self):
        if self.current_media_files:
            file_path, media_type = self.current_media_files[self.image_index]
            self.grow_image(file_path)
            self.update_button_state()

    def grow_image(self, file_path):
        try:
            img = Image.open(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            return

        initial_size = (50, 50)
        self.is_animating = True

        def resize_image(step):
            if step <= 100:
                new_width = int(initial_size[0] + (self.max_image_size[0] - initial_size[0]) * (step / 100))
                new_height = int(initial_size[1] + (self.max_image_size[1] - initial_size[1]) * (step / 100))

                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(resized_img)

                self.image_label.config(image=img_tk)
                self.image_label.image = img_tk
                self.image_label.pack(expand=True)

                self.after(self.animation_speed, resize_image, step + 2)
            else:
                self.is_animating = False
                if self.slideshow_running:
                    self.after(2000, self.show_next_image)

        resize_image(0)

    def play_audio_for_category(self, category):
        pygame.mixer.stop()

        audio_folder = self.category_audio_map.get(category)
        if audio_folder:
            audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]
            if audio_files:
                pygame.mixer.music.load(os.path.join(audio_folder, audio_files[0]))
                pygame.mixer.music.play(-1)

    def show_next_image(self):
        if self.current_media_files and not self.is_animating:
            self.image_index = (self.image_index + 1) % len(self.current_media_files)
            self.show_image()

    def show_previous_image(self):
        if self.current_media_files and not self.is_animating:
            self.image_index = (self.image_index - 1) % len(self.current_media_files)
            self.show_image()

    def update_button_state(self):
        if self.current_media_files:
            self.prev_button.config(state=tk.NORMAL if self.image_index > 0 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.image_index < len(self.current_media_files) - 1 else tk.DISABLED)
        else:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

    def toggle_slideshow(self):
        if self.slideshow_running:
            self.slideshow_running = False
            self.slideshow_button.config(text="Resume Slideshow")
            pygame.mixer.music.stop()
        else:
            self.slideshow_running = True
            self.slideshow_button.config(text="Pause Slideshow")
            self.run_slideshow()

    def run_slideshow(self):
        if self.slideshow_running and self.current_media_files and not self.is_animating:
            self.show_next_image()
            self.after(3000, self.run_slideshow)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            pygame.mixer.music.stop()  # Stop music on exit
            self.destroy()


if __name__ == "__main__":
    app = MediaViewer()
    app.mainloop()
