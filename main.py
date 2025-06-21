import tkinter as tk
from tkinter import messagebox
import time
import json
import os # Import the os module to check for file existence

class SubtractGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Subtract by 7 from 100 to 0")
        self.geometry("400x150")
        self.resizable(False, False)

        self.start_value = 100
        self.subtract_value = 7
        self.current_value = self.start_value

        # --- Changes for Timer and Personal Best ---
        self.timer_running = True # Flag to control timer
        self.start_time = time.time() # Record start time
        self.elapsed_time = 0.0 # To store the final elapsed time

        self.pbest_file = "personal_best.json" # File name for personal best
        self.personal_best = self.load_personal_best() # Load personal best at start
        # --- End Changes ---

        self.create_widgets()

        # Enter-Taste bindet an check_input
        self.entry.bind('<Return>', lambda event: self.check_input())

        self.update_timer() # Start the timer update loop

    def create_widgets(self):
        self.value_label = tk.Label(self, text=f"Current Number: {self.current_value}", font=("Arial", 14))
        self.value_label.pack(pady=(10, 5))

        entry_frame = tk.Frame(self)
        entry_frame.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(entry_frame, textvariable=self.entry_var, width=10, font=("Arial", 14))
        self.entry.pack(side=tk.LEFT)
        self.entry.focus()

        self.feedback_label = tk.Label(entry_frame, text="", font=("Arial", 14))
        self.feedback_label.pack(side=tk.LEFT, padx=(10,0))

        self.submit_btn = tk.Button(self, text="Check Input", command=self.check_input, font=("Arial", 12))
        self.submit_btn.pack(pady=(10,0))

        self.timer_label = tk.Label(self, text="Time: 0.0s", font=("Arial", 10))
        self.timer_label.place(x=10, y=130)

    # --- New Methods for Personal Best Management ---
    def load_personal_best(self):
        """Loads the personal best time from a JSON file."""
        if os.path.exists(self.pbest_file):
            try:
                with open(self.pbest_file, "r") as f:
                    data = json.load(f)
                    return data.get("best_time", None) # Return best_time or None if not found
            except Exception:
                # Handle cases where the file might be corrupted
                return None
        return None # Return None if file does not exist

    def save_personal_best(self, best_time):
        """Saves the new personal best time to a JSON file."""
        try:
            with open(self.pbest_file, "w") as f:
                json.dump({"best_time": best_time}, f)
        except Exception as e:
            messagebox.showerror("Error", f"Error when saving your personal best:\n{e}")
    # --- End New Methods ---

    def check_input(self):
        inp = self.entry_var.get().strip()
        try:
            val = int(inp)
        except ValueError:
            self.set_feedback(False)
            self.entry_var.set("")
            return

        expected = self.current_value - self.subtract_value
        if expected < 0:
            self.set_feedback(False, message="Cannot subtract any further.")
            self.entry_var.set("")
            return

        if val == expected:
            self.current_value = val
            self.value_label.config(text=f"Current Number: {self.current_value}")
            self.set_feedback(True)
            self.entry_var.set("")

            # --- Logic to stop timer and handle personal best at 2 ---
            # Check if we reached the maximum of 2 (as per your query)
            if self.current_value == 2:
                self.stop_timer() # Stop the timer
                self.submit_btn.config(state=tk.DISABLED) # Disable input
                self.entry.config(state=tk.DISABLED)
                self.set_feedback(True, message="Maximum Number (2) reached! Game over.")

                # Check and update personal best
                if (self.personal_best is None) or (self.elapsed_time < self.personal_best):
                    self.save_personal_best(self.elapsed_time)
                    messagebox.showinfo("New Personal Best!", f"Congratulations!\nNew Personal Best Time: {self.elapsed_time:.2f}s")
                else:
                    messagebox.showinfo("Info", f"Your Time: {self.elapsed_time:.2f}s\nPersonal Best: {self.personal_best:.2f}s")
            # --- End Logic for Timer Stop and Personal Best ---
            else:
                # Original logic: Also check if next subtract is less than zero, then disable input
                if self.current_value - self.subtract_value < 0:
                    self.submit_btn.config(state=tk.DISABLED)
                    self.entry.config(state=tk.DISABLED)
                    self.set_feedback(True, message="Cannot substract any further.")
        else:
            self.set_feedback(False)
            self.entry_var.set("")

    def set_feedback(self, success, message=None):
        if success:
            self.feedback_label.config(text="\u2714", fg="green")  # ✔
            if message:
                messagebox.showinfo("Info", message)
        else:
            self.feedback_label.config(text="\u2718", fg="red")  # ✘
            if message:
                messagebox.showerror("Error", message)

    # --- Modified Timer Methods ---
    def update_timer(self):
        """Updates the timer display if the timer is running."""
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time # Calculate elapsed time
            self.timer_label.config(text=f"Zeit: {self.elapsed_time:.1f}s")
            self.after(100, self.update_timer) # Schedule next update

    def stop_timer(self):
        """Stops the timer from updating."""
        self.timer_running = False
    # --- End Modified Timer Methods ---

if __name__ == "__main__":
    app = SubtractGame()
    app.mainloop()