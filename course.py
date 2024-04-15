import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class CourseInformationSystemGUI:
    def __init__(self, root):
        self.root = root

        self.create_title_label()

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="COURSE REGISTRATION",
            font=("Arial", 35, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=89
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        self.csv_filename = "courses.csv"
        self.fields = ["courseCode", "courseTitle"]

        self.coursecode_label = tk.Label(self.root, text="Course Code:", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.coursecode_label.place(x=80, y=100)
        self.coursecode_entries = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.coursecode_entries.place(x=230, y=100, width=180)

        self.coursetitle_label = tk.Label(self.root, text="Course Title:", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.coursetitle_label.place(x=440, y=100)
        self.coursetitle_entries = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.coursetitle_entries.place(x=590, y=100, width=400)

        self.tosearch_label = tk.Label(self.root, text="To Search for Student Information:", font=("Arial", 17, "bold"), bg="#A6A6A6", fg="black")
        self.tosearch_label.place(x=80, y=300)

        self.search_label = tk.Label(self.root, text="Enter Keyword to Search:", font=("Arial", 17), bg="#A6A6A6", fg="black")
        self.search_label.place(x=130, y=340)

        self.search_entry = tk.Entry(self.root, font=("Arial", 17), bg="white", fg="black")
        self.search_entry.place(x=410, y=340, width=420)

#----------------------------------------------------- BUTTONS --------------------------------------------------------
            
        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.add_course)
        self.add_button.place(x=250, y=200, width=250)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.delete_course)
        self.delete_button.place(x=250, y=250, width=250)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.edit_course)
        self.edit_button.place(x=600, y=200, width=250)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.save_changes)
        self.save_button.place(x=600, y=250, width=250)

        # Search Button
        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.search_course)
        self.search_button.place(x=850, y=340, width=130)

        # Cancel button
        self.cancel_button = tk.Button(self.root, text="CANCEL", font=("Arial", 13, "bold"), bg="#2E2D2D", fg="white", command=self.cancel_edit)
        self.cancel_button.place(x=350, y=150, width=350)

#--------------------------------------------------------------- TREEVIEW --------------------------------------------------------

        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("Course Code","Course Title"), show="headings")

        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Title", text="Course Title")

        self.tree.column("Course Code", width=30)
        self.tree.column("Course Title", width=100)
        self.tree.place(x=200, y=400, width=700, height=250)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", background="#2E2D2D",  foreground="white", font=("Arial", 12, "bold"))

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=900, y=400, height=250)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Load existing courses
        self.load_courses()

        self.selected_item = None

    def edit_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Store the selected item for later use
        self.selected_item = selected_item

        # Extract course information from the selected item
        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        # Display course information in entry fields for editing
        self.coursecode_entries.delete(0, "end")
        self.coursecode_entries.insert(0, course_values[0])

        self.coursetitle_entries.delete(0, "end")
        self.coursetitle_entries.insert(0, course_values[1])

    def clear_entry_fields(self):
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def cancel_edit(self):
        self.selected_item = None
        self.clear_entry_fields()
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Retrieve edited values from entry fields
        edited_course_code = self.coursecode_entries.get()
        edited_course_title = self.coursetitle_entries.get()

        # Check if any field is empty
        if edited_course_code == '' or edited_course_title == '':
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        selected_course_code = self.tree.item(self.selected_item, "values")[0]

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=(edited_course_code, edited_course_title))

        # Update CSV file with the edited values
        self.update_csv(selected_course_code, edited_course_code, edited_course_title)

        self.selected_item = None

        # Clear entry fields
        self.clear_entry_fields()

        messagebox.showinfo("Success", "Changes saved successfully!")

    def update_csv(self, selected_course_code, edited_course_code, edited_course_title):
        data = []
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        for row in data:
            if row[0] == selected_course_code:
                row[0] = edited_course_code
                row[1] = edited_course_title
                break

        # Write the updated data back to the CSV file
        with open(self.csv_filename, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

    def load_courses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load courses from CSV file
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.tree.insert("", "end", values=(row[0], row[1]))

    def add_course(self):
        values = [self.coursecode_entries.get(), self.coursetitle_entries.get()]

        # Check if any field is empty
        if any(value == '' for value in values):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        # Check if course code already exists
        course_code = values[0]
        if self.check_course(course_code):
            messagebox.showerror("Error", f"Course {course_code} already exists.")
            return

        # Write to CSV file
        with open(self.csv_filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(values)

        # Update Treeview
        self.tree.insert("", "end", values=values)

        # Clear entry fields
        self.coursecode_entries.delete(0, "end")
        self.coursetitle_entries.delete(0, "end")

        messagebox.showinfo("Success", "Course added successfully!")

    def delete_course(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a course to delete.")
            return

        course_values = self.tree.item(selected_item, "values")
        if not course_values:
            messagebox.showwarning("Warning", "Selected item does not contain course information.")
            return

        course_code = course_values[0]
        self.tree.delete(selected_item)

        self.delete_course_from_csv(course_code)

        messagebox.showinfo("Success", f"Course {course_code} deleted successfully!")

    def check_course(self, course_code):
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=self.fields)
            for row in csvreader:
                if course_code.lower() == str(row["courseCode"]).lower():
                    return True
        return False

    def delete_course_from_csv(self, course_code):
        data = []
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=self.fields)
            for row in csvreader:
                if row["courseCode"].lower() != course_code.lower():
                    data.append(row)

        # Write the data back to the CSV file
        with open(self.csv_filename, "w", newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=self.fields)
            csvwriter.writerows(data)

        # Update corresponding course code to "N/A" in the student CSV file
        student_data = []
        with open("students.csv", "r") as student_file:
            student_reader = csv.reader(student_file)
            for student_row in student_reader:
                if student_row[3] == course_code:  # If the student's course code matches the deleted course code
                    student_row[3] = "N/A"  # Set course code to "N/A"
                student_data.append(student_row)

        # Write the updated student data back to the CSV file
        with open("students.csv", "w", newline='') as student_file:
            student_writer = csv.writer(student_file)
            student_writer.writerows(student_data)

    def search_course(self, event=None):
        keyword = self.search_entry.get().lower()

        if not keyword.strip():
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        # Clear previous selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Highlight rows matching the search keyword
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(keyword in value.lower() for value in values):
                self.tree.selection_add(item)

def main():
    root = tk.Tk()
    root.title("Course Registration")
    root.configure(bg="#A6A6A6")
    root.geometry("1070x675") 
    root.resizable(False, False) 

    course_app = CourseInformationSystemGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
