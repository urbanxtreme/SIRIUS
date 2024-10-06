import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Ensure Pillow is installed for image handling

# Quiz data
quiz_data = [
    {"question": "What is the primary mirror of JWST made of?",
     "options": ["Gold", "Beryllium", "Silver", "Copper"], "answer": 1},
    {"question": "Which planet will JWST primarily observe?",
     "options": ["Mars", "Jupiter", "Exoplanets", "Venus"], "answer": 2},
    {"question": "In what year was the JWST launched?",
     "options": ["2015", "2020", "2021", "2022"], "answer": 3},
    {"question": "What does JWST stand for?",
     "options": ["James Webb Space Telescope", "John Wayne Space Telescope",
                 "James West Space Telescope", "Jupiter Wide Space Telescope"], "answer": 0},
    {"question": "What is the main purpose of JWST?",
     "options": ["Studying exoplanets", "Observing black holes", "Mapping the Milky Way",
                 "Studying cosmic inflation"], "answer": 0},
    {"question": "What type of telescope is JWST?",
     "options": ["Radio telescope", "Optical telescope", "Infrared telescope",
                 "X-ray telescope"], "answer": 2},
    {"question": "Where is JWST positioned?",
     "options": ["Low Earth Orbit", "Lunar Orbit", "L2 Lagrange Point", "Mars Orbit"], "answer": 2},
    {"question": "Who is the JWST named after?",
     "options": ["James Webb", "Albert Einstein", "Galileo Galilei", "Neil Armstrong"], "answer": 0},
    {"question": "How many segments does the primary mirror of JWST have?",
     "options": ["5", "9", "12", "18"], "answer": 3},
    {"question": "What does the sunshield of JWST do?",
     "options": ["Reflects sunlight", "Keeps instruments cool", "Provides power",
                 "Stabilizes the telescope"], "answer": 1},
]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JWST Quiz")

        # Use the root instance to get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window geometry to full screen size
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')

        # Load the image
        self.background_image = Image.open("img.jpg")  # Load your image file
        self.background_image = self.background_image.resize((screen_width, screen_height),
                                                             Image.LANCZOS)  # Resize to fit the screen
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a Canvas widget to hold the image
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Set the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Create buttons directly on the canvas
        self.submit_button = tk.Button(self.canvas, text="Submit", command=self.submit_answer, font=("Helvetica", 20),
                                       bg='green', fg='white')
        self.submit_button.place(relx=0.5, rely=0.4, anchor='center')  # Centered position

        self.retry_button = tk.Button(self.canvas, text="Retry", command=self.retry_quiz, font=("Helvetica", 20),
                                      bg='yellow', fg='black')
        self.retry_button.place(relx=0.5, rely=0.5, anchor='center')  # Centered position

        self.quit_button = tk.Button(self.canvas, text="Quit", command=self.confirm_quit, font=("Helvetica", 20),
                                     bg='red', fg='white')
        self.quit_button.place(relx=0.5, rely=0.6, anchor='center')  # Centered position

        # Initialize the quiz state
        self.score = 0
        self.question_index = 0
        self.user_answers = []
        self.options_var = tk.IntVar()
        self.option_buttons = []

        self.update_question()  # Start the quiz by updating the question

    def update_question(self):
        # Clear any existing option buttons
        for btn in self.option_buttons:
            btn.destroy()
        self.option_buttons.clear()

        if self.question_index < len(quiz_data):
            current_question = quiz_data[self.question_index]
            question_label = tk.Label(self.canvas, text=current_question["question"], font=("Helvetica", 24),
                                      bg='systemTransparent', fg='black')  # Transparent background
            question_label.place(relx=0.5, rely=0.25, anchor='center')  # Centered position

            # Create new option buttons
            for i, option in enumerate(current_question["options"]):
                btn = tk.Radiobutton(self.canvas, text=option, variable=self.options_var, value=i,
                                     font=("Helvetica", 20), bg='cyan', fg='black', activebackground='lightblue',
                                     selectcolor='red')
                btn.place(relx=0.5, rely=0.35 + (i * 0.05), anchor='center')  # Stacked vertically
                self.option_buttons.append(btn)
            self.options_var.set(-1)  # Reset selected option
        else:
            self.display_results()

    def submit_answer(self):
        selected_option = self.options_var.get()
        if selected_option != -1:
            correct_answer = quiz_data[self.question_index]["answer"]
            self.user_answers.append((quiz_data[self.question_index]["options"][selected_option],
                                      quiz_data[self.question_index]["options"][correct_answer]))
            if selected_option == correct_answer:
                self.score += 1
            self.question_index += 1
            self.update_question()
        else:
            messagebox.showwarning("Warning", "Please select an option.")

    def display_results(self):
        # Clear existing widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()

        result_label = tk.Label(self.canvas, text="Quiz Completed!", font=("Helvetica", 32), bg='systemTransparent',
                                fg='black')  # Transparent background
        result_label.place(relx=0.5, rely=0.4, anchor='center')  # Centered position

        score_label = tk.Label(self.canvas, text=f"Your Score: {self.score}/{len(quiz_data)}", font=("Helvetica", 24),
                               bg='systemTransparent', fg='black')  # Transparent background
        score_label.place(relx=0.5, rely=0.5, anchor='center')  # Centered position

        # Display answers
        for i, (user_answer, correct_answer) in enumerate(self.user_answers):
            color = "green" if user_answer == correct_answer else "red"
            result_line = tk.Label(self.canvas,
                                   text=f"Q{i + 1}: {user_answer} - {'Correct' if user_answer == correct_answer else 'Wrong'}",
                                   font=("Helvetica", 20), bg='systemTransparent', fg=color)  # Transparent background
            result_line.place(relx=0.5, rely=0.55 + (i * 0.05), anchor='center')  # Stacked vertically

    def retry_quiz(self):
        self.score = 0
        self.question_index = 0
        self.user_answers = []
        self.update_question()  # Restart the quiz

    def confirm_quit(self):
        if messagebox.askyesno("Confirm Quit", "Are you sure you want to quit?"):
            self.root.quit()


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
