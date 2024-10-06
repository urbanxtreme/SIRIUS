import tkinter as tk
import os
import webbrowser
import subprocess  # Import subprocess module
from PIL import Image, ImageTk

class FullScreenWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SIRIUS")

        # Set the window icon
        logo_image = Image.open("logo.png")
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.iconphoto(False, logo_photo)

        # Maximize the window to fill the screen
        self.state('zoomed')

        # Load and set the background image
        self.image = Image.open("JWST.jpg")
        self.image = self.image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label to display the background image
        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Create a label at the top center for software name
        self.title_label = tk.Label(self, text="SIRIUS", font=('Arial', 28, 'bold'), bg='dark blue', fg='white')
        self.title_label.place(relx=0.5, y=30, anchor="center")

        # Create buttons at the bottom left with improved styling
        self.create_buttons()

        # Bind the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_buttons(self):
        # Button styling with hover and shadow effects
        button_style = {
            'font': ('Arial', 14, 'bold'),
            'bg': '#808080',  # Grey background
            'fg': 'lime',    # Lime text
            'activebackground': '#666666',  # Darker grey when clicked
            'activeforeground': 'lime',    # Keep lime text when clicked
            'width': 18,      # Increased button width for better proportions
            'height': 2       # Button height
        }

        def on_enter(e):
            e.widget['bg'] = '#666666'

        def on_leave(e):
            e.widget['bg'] = '#808080'

        self.button1 = tk.Button(self, text="About JWST", command=self.on_button1_click, **button_style)
        self.button1.place(x=100, y=self.winfo_screenheight() - 500)
        self.button1.bind("<Enter>", on_enter)
        self.button1.bind("<Leave>", on_leave)

        self.button2 = tk.Button(self, text="Solar Expo", command=self.on_button2_click, **button_style)
        self.button2.place(x=100, y=self.winfo_screenheight() - 350)
        self.button2.bind("<Enter>", on_enter)
        self.button2.bind("<Leave>", on_leave)

        self.button3 = tk.Button(self, text="3-D JWST", command=self.on_button3_click, **button_style)
        self.button3.place(x=100, y=self.winfo_screenheight() - 200)
        self.button3.bind("<Enter>", on_enter)
        self.button3.bind("<Leave>", on_leave)

        self.button4 = tk.Button(self, text="JWST Quiz", command=self.on_button4_click, **button_style)
        self.button4.place(x=self.winfo_screenwidth() - 350, y=self.winfo_screenheight() - 500)
        self.button4.bind("<Enter>", on_enter)
        self.button4.bind("<Leave>", on_leave)

        self.button5 = tk.Button(self, text="Feedback", command=self.on_button5_click, **button_style)
        self.button5.place(x=self.winfo_screenwidth() - 350, y=self.winfo_screenheight() - 350)
        self.button5.bind("<Enter>", on_enter)
        self.button5.bind("<Leave>", on_leave)

        self.button6 = tk.Button(self, text="Before the birth", command=self.on_button6_click, **button_style)
        self.button6.place(x=self.winfo_screenwidth() - 350, y=self.winfo_screenheight() - 200)
        self.button6.bind("<Enter>", on_enter)
        self.button6.bind("<Leave>", on_leave)

        self.button7 = tk.Button(self, text="Explore The Horizon", command=self.on_button7_click, width=20, height=2,
                                 font=('Arial', 14, 'bold'), bg='#808080', fg="lime", activebackground='#666666',
                                 activeforeground='lime')
        self.button7.place(x=self.winfo_screenwidth() // 2 - 150, y=self.winfo_screenheight() - 150)
        self.button7.bind("<Enter>", on_enter)
        self.button7.bind("<Leave>", on_leave)

        self.bind("<Configure>", self.update_button_positions)

    def on_button1_click(self):
        print("Button 1 clicked")

    def on_button2_click(self):
        print("Button 2 clicked")

    def on_button3_click(self):
        html_file_path = os.path.abspath("index.html")
        webbrowser.open(f"file://{html_file_path}")

    def on_button4_click(self):
        # Run gamenew.py using subprocess
        script_path = os.path.abspath("gamenew.py")
        subprocess.run(["python", script_path], check=True)  # Launch gamenew.py

    def on_button5_click(self):
        print("Button 5 clicked")

    def on_button6_click(self):
        print("Button 6 clicked")

    def on_button7_click(self):
        print("Main Action clicked")

    def on_close(self):
        self.destroy()

    def update_button_positions(self, event=None):
        height = self.winfo_height()
        width = self.winfo_width()
        self.button1.place(x=100, y=height - 500)
        self.button2.place(x=100, y=height - 350)
        self.button3.place(x=100, y=height - 200)
        self.button4.place(x=width - 350, y=height - 500)
        self.button5.place(x=width - 350, y=height - 350)
        self.button6.place(x=width - 350, y=height - 200)
        self.button7.place(x=width // 2 - 150, y=height - 150)

if __name__ == "__main__":
    app = FullScreenWindow()
    app.mainloop()
