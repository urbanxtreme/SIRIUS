import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")

        # Set the full-screen background image
        self.image = Image.open("img.jpg")  # Ensure this path is correct
        self.image = self.image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label to display the image
        self.image_label = tk.Label(self.root, image=self.photo)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # Initialize variables
        self.score = 0
        self.question_index = 0
        self.remaining_time = 15
        self.user_answers = []
        self.selected_option = None
        self.timer_running = False  # To track if the timer is active
        self.timer_id = None  # Store the timer ID to cancel it if necessary

        # Create UI elements
        self.timer_label = tk.Label(self.root, text="", font=("Helvetica", 16), bg='white', fg='black')  # Timer label
        self.timer_label.place(relx=0.5, y=50, anchor="center")  # Position the timer at the top center

        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 24), bg='white', fg='black')  # Changed bg color
        self.question_label.place(relx=0.5, y=120, anchor="center")  # Adjusted position

        self.option_buttons = []
        button_height = 2
        button_width = 30  # Set a specific width to accommodate text

        for i in range(4):
            btn = tk.Button(self.root, text="", font=("Helvetica", 20), bg='lightgray', fg='black',
                            command=lambda idx=i: self.select_option(idx), height=button_height, width=button_width)
            btn.place(relx=0.5, y=200 + i * (100), anchor='center')  # Adjusted vertical space (100)
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_answer,
                                       font=("Helvetica", 20), bg='green', fg='white', height=button_height, width=button_width)
        self.submit_button.place(relx=0.5, y=600, anchor="center")  # Adjusted position to accommodate new spacing

        # Start the quiz
        self.update_question()

    def update_question(self):
        if self.question_index < len(quiz_data):
            current_question = quiz_data[self.question_index]
            self.question_label.config(text=current_question["question"])
            for i, option in enumerate(current_question["options"]):
                self.option_buttons[i].config(text=option, bg='lightgray')  # Reset button background
            self.selected_option = None  # Reset selected option
            self.remaining_time = 15  # Reset remaining time for the new question
            self.update_timer_label()  # Update the timer label with the new time
            self.start_timer()  # Restart the timer for the new question
        else:
            self.clear_question_elements()  # Clear question elements before showing results
            self.display_results()

    def clear_question_elements(self):
        """Hide the question and option buttons before displaying results."""
        self.question_label.place_forget()  # Remove question label
        for btn in self.option_buttons:
            btn.place_forget()  # Remove option buttons
        self.submit_button.place_forget()  # Remove submit button
        self.timer_label.place_forget()  # Remove timer label

    def select_option(self, idx):
        # Highlight selected option
        if self.selected_option is not None:
            self.option_buttons[self.selected_option].config(bg='lightgray')  # Reset previous selection
        self.selected_option = idx
        self.option_buttons[idx].config(bg='yellow')  # Highlight the selected button

    def submit_answer(self):
        if self.question_index < len(quiz_data):  # Check if there are more questions
            if self.selected_option is not None:
                correct_answer = quiz_data[self.question_index]["answer"]
                self.user_answers.append((quiz_data[self.question_index]["options"][self.selected_option],
                                           quiz_data[self.question_index]["options"][correct_answer]))
                if self.selected_option == correct_answer:
                    self.score += 1
                self.question_index += 1
                self.update_question()  # Automatically update question
            else:
                messagebox.showwarning("Warning", "Please select an option.")
        else:
            self.clear_question_elements()  # Clear question elements before showing results
            self.display_results()  # If no more questions, display results

    def start_timer(self):
        if not self.timer_running:  # Start timer only if not already running
            self.timer_running = True  # Start the timer
            self.update_timer()  # Begin updating the timer

    def update_timer(self):
        if self.remaining_time > 0:
            self.update_timer_label()  # Update the timer label with remaining time
            self.remaining_time -= 1
            self.timer_id = self.root.after(1000, self.update_timer)  # Schedule the next timer update
        else:
            self.stop_timer()  # Stop the timer and handle time-up logic
            self.submit_answer()  # Automatically submit when time is up

    def stop_timer(self):
        if self.timer_id is not None:  # Cancel any existing timer
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.timer_running = False  # Stop further updates

    def update_timer_label(self):
        self.timer_label.config(text=f"Time Left: {self.remaining_time} seconds")

    def display_results(self):
        # Display results
        result_label = tk.Label(self.root, text="Quiz Completed!", font=("Helvetica", 32), bg='white', fg='black')  # Changed bg color
        result_label.place(relx=0.5, y=200, anchor="center")  # Adjusted Y position for better visibility

        score_label = tk.Label(self.root, text=f"Your Score: {self.score}/{len(quiz_data)}",
                                font=("Helvetica", 24), bg='white', fg='black')  # Changed bg color
        score_label.place(relx=0.5, y=260, anchor="center")  # Adjusted Y position for better visibility

        results_frame = tk.Frame(self.root, bg='white')  # Create a frame for results
        results_frame.place(relx=0.5, y=300, anchor="center")  # Adjusted Y position for better visibility

        for i, (user_answer, correct_answer) in enumerate(self.user_answers):
            color = "green" if user_answer == correct_answer else "red"
            result_line = tk.Label(results_frame,
                                    text=f"Q{i + 1}: {user_answer} - {'Correct' if user_answer == correct_answer else 'Wrong'}",
                                    font=("Helvetica", 18), bg='white', fg=color)  # Changed bg color
            result_line.pack(pady=5)  # Add vertical space between results

        # Add a Quit button at the end
        quit_button = tk.Button(self.root, text="Quit", command=self.root.quit,
                                font=("Helvetica", 20), bg='red', fg='white')
        quit_button.place(relx=0.5, y=600, anchor="center")  # Position the Quit button

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    game.run()
