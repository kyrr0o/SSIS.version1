import tkinter as tk
from tkinter import messagebox
from student import StudentInformationSystemGUI
from course import CourseInformationSystemGUI

class SimpleStudentInformationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Student Information System")
        self.configure(bg="#DDDDDD")
        self.geometry("650x350")
        self.resizable(False, False)

        self.create_title_label()
        self.create_buttons()

    def create_title_label(self):
        title_label = tk.Label(
            self,
            text="STUDENT INFORMATION SYSTEM",
            font=("Arial", 25, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            foreground="white"
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        registration_label = tk.Label(
            self,
            text="Choose Registration Option:",
            font=("Arial", 15),
            bg="#DDDDDD",
            foreground="black"
        )
        registration_label.place(x=25, y=80)

    def create_buttons(self):
        student_button = tk.Button(
            self,
            text="STUDENT REGISTRATION",
            font=("Arial", 15, "bold"),
            bg="#2E2D2D",
            foreground="white",
            command=self.open_student_information
        )
        student_button.place(x=180, y=130, width=300)

        course_button = tk.Button(
            self,
            text="COURSE REGISTRATION",
            font=("Arial", 15, "bold"),
            bg="#2E2D2D",
            foreground="white",
            command=self.open_course_information
        )
        course_button.place(x=180, y=200, width=300)

        exit_btn = tk.Button(
            self,
            text="EXIT",
            font=("Arial", 15, "bold"),
            bg="#2E2D2D",
            foreground="white",
            command=self.destroy
        )
        exit_btn.place(x=180, y=270, width=300)

    def open_student_information(self):
        self.withdraw()
        student_root = tk.Toplevel(self)
        student_root.title("Student Registration")
        student_root.configure(bg="#DDDDDD")
        student_root.geometry("600x650") 
        student_root.resizable(False, False)
        student_root.protocol("WM_DELETE_WINDOW", lambda: self.close_window(student_root))
        student_app = StudentInformationSystemGUI(student_root)

    def open_course_information(self):
        self.withdraw()
        course_root = tk.Toplevel(self)
        course_root.title("Course Information System")
        course_root.configure(bg="#DDDDDD")
        course_root.geometry("550x600") 
        course_root.resizable(False, False) 
        course_root.protocol("WM_DELETE_WINDOW", lambda: self.close_window(course_root))
        course_app = CourseInformationSystemGUI(course_root)

    def close_window(self, window):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
            self.deiconify()

def main():
    app = SimpleStudentInformationSystem()
    app.mainloop()

if __name__ == "__main__":
    main()
