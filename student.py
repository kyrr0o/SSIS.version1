import csv
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class StudentInformationSystemGUI:
    def __init__(self, root):

        self.root = root

        # Create title label
        self.create_title_label()
        self.gender_options = ["Male", "Female", "Other"]
        self.gender_var = tk.StringVar(self.root)

    def check_course_code(self, course_code):
        with open("courses.csv", "r") as course_file:
            csvreader = csv.reader(course_file)
            for row in csvreader:
                if row[0] == course_code:
                    return True
        return False

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="STUDENT REGISTRATION",
            font=("Arial", 25, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=89
        )
        title_label.grid(row=0, column=0, columnspan=1, sticky='ew')

        self.csv_filename = "students.csv"
        self.fields = ["idNum", "firstName", "lastName", "gender", "course", "yearLevel"]

        # Labels and Entry fields
        self.labels = ["Student ID", "First Name", "Last Name", "Gender", "Year Level", "Course Code"]
        self.entries = {label: tk.Entry(self.root, font=("Arial", 14,), bg="white", fg="black") for label in self.labels}

        self.tosearch_label = tk.Label(self.root, text="To Search for Student Information:", font=("Arial", 14, "bold"), bg="#DDDDDD", fg="black")
        self.tosearch_label.place(x=20, y=365)

        self.search_label = tk.Label(self.root, text="Enter Course Code:", font=("Arial", 14), bg="#DDDDDD", fg="black")
        self.search_label.place(x=50, y=395)

        # Place labels and entry fields on the GUI
        x_label_position = 20
        x_entry_position = 170
        y_start_position = 70
        y_increment = 50
        entry_width = 250

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(
                self.root, text=label, font=("Arial", 14, "bold"), bg="#DDDDDD", fg="black"
            )
            label_widget.place(x=x_label_position, y=y_start_position + i * y_increment)

            entry_widget = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
            entry_widget.place(x=x_entry_position, y=y_start_position + i * y_increment, width=entry_width)
            self.entries[label] = entry_widget

        # Gender dropdown
        self.gender_label = tk.Label(self.root, text="Gender", font=("Arial", 14, "bold"), bg="#DDDDDD", fg="black")
        self.gender_label.place(x=x_label_position, y=y_start_position + 3 * y_increment)

        self.gender_variable = tk.StringVar(self.root)
        self.gender_variable.set("Male")  # Default value
        self.gender_dropdown = tk.OptionMenu(self.root, self.gender_variable, "Male", "Female", "Other")
        self.gender_dropdown.config(font=("Arial", 12), bg="white", fg="black")
        self.gender_dropdown.place(x=x_entry_position, y=y_start_position + 3 * y_increment, width=entry_width)

#----------------------------------------------------- BUTTONS --------------------------------------------------------

        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), command=self.add_student)
        self.add_button.place(x=450, y=100, width=125)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), command=self.edit_student)
        self.edit_button.place(x=450, y=150, width=125)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), command=self.save_changes)
        self.save_button.place(x=450, y=200, width=125)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), command=self.delete_student)
        self.delete_button.place(x=450, y=250, width=125)

        # Search Entry and Button
        self.search_entry = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.search_entry.place(x=230, y=400, width=190)

        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), command=self.search_student)
        self.search_button.place(x=450, y=398, width=125)

#--------------------------------------------------------------- TREEVIEW --------------------------------------------------------
        
        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID Number", "First Name", "Last Name", "Gender", "Course", "Year Level"), show="headings")

        self.tree.heading("ID Number", text="ID Number")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Year Level", text="Year Level")

        self.tree.column("ID Number", width=100)
        self.tree.column("First Name", width=100)
        self.tree.column("Last Name", width=100)
        self.tree.column("Gender", width=100)
        self.tree.column("Course", width=100)
        self.tree.column("Year Level", width=100)
        self.tree.place(x=10, y=440, width=580, height=200)

        self.load_students()

        self.selected_item = None

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        self.selected_item = selected_item

        student_values = self.tree.item(selected_item, "values")
        if not student_values:
            messagebox.showwarning("Warning", "Selected item does not contain student information.")
            return

        # Populate entry fields with student information
        self.entries["Student ID"].delete(0, "end")
        self.entries["Student ID"].insert(0, student_values[0])

        self.entries["First Name"].delete(0, "end")
        self.entries["First Name"].insert(0, student_values[1])

        self.entries["Last Name"].delete(0, "end")
        self.entries["Last Name"].insert(0, student_values[2])

        self.gender_variable.set(student_values[3])

        self.entries["Course Code"].delete(0, "end")
        self.entries["Course Code"].insert(0, student_values[4])

        self.entries["Year Level"].delete(0, "end")
        self.entries["Year Level"].insert(0, student_values[5])

    def clear_entry_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        # Retrieve edited values from entry fields and dropdown
        edited_values = [
            self.entries["Student ID"].get(),
            self.entries["First Name"].get(),
            self.entries["Last Name"].get(),
            self.gender_variable.get(),
            self.entries["Course Code"].get(),
            self.entries["Year Level"].get()
        ]

        # Course Code Checker
        if not self.check_course_code(edited_values[4]):
            messagebox.showwarning("Warning", f"Course {edited_values[4]} does not exist.")
            return

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=edited_values)

        self.selected_item = None

        # Update the corresponding entry in the CSV file
        self.update_student_in_csv(edited_values)

        # Clear entry fields
        self.clear_entry_fields()

    def update_student_in_csv(self, edited_values):
        data = []
        with open(self.csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != edited_values[0]:
                    data.append(row)
                else:
                    data.append([edited_values[0], edited_values[1], edited_values[2], edited_values[3], edited_values[4], edited_values[5]])

        # Write the updated data back to the CSV file
        with open(self.csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                self.tree.insert("", "end", values=row)

    def check_IDNo(self, idNo):
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.DictReader(csvfile, fieldnames=self.fields)
            for row in csvreader:
                if idNo == row["idNum"]:
                    return True
        return False

    def add_student(self):
        first_name = self.entries["First Name"].get()
        last_name = self.entries["Last Name"].get()
        idNo = self.entries["Student ID"].get()
        yr_level = self.entries["Year Level"].get()
        course_code = self.entries["Course Code"].get()
        gender = self.gender_variable.get()

        if any(value == '' for value in [first_name, last_name, idNo, yr_level, course_code, gender]):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if self.check_IDNo(idNo):
            messagebox.showerror("Error", f"Student {idNo} already exists.")
            return

        # Course Code Checker
        if not self.check_course_code(course_code):
            messagebox.showwarning("Warning", f"Course {course_code} does not exist.")
            return

        # Update Treeview
        self.tree.insert("", "end", values=[idNo, first_name, last_name, gender, course_code, yr_level])

        # Write to CSV file
        with open(self.csv_filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([idNo, first_name, last_name, gender, course_code, yr_level])

        # Clear entry fields
        for entry in self.entries.values():
            entry.delete(0, "end")

        messagebox.showinfo("Success", "Student added successfully!")

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete.")
            return

        # Delete each selected item individually
        for item in selected_item:
            student_values = self.tree.item(item, "values")
            if not student_values:
                continue  # Skip if there are no values

            student_id = student_values[0]

            # Delete the selected item from the Treeview
            self.tree.delete(item)

            # Delete the corresponding entry from the CSV file
            self.delete_student_from_csv(student_id)

        messagebox.showinfo("Success", "Selected student(s) deleted successfully!")

    def delete_student_from_csv(self, student_id):
        data = []
        with open(self.csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != student_id: 
                    data.append(row)

        # Write the updated data back to the CSV file
        with open(self.csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def search_student(self):
        search_key = self.search_entry.get().strip().lower()

        # Clear previous selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)

        # Highlight rows matching the search keyword
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(search_key in value.lower() for value in values):
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)

def main():
    root = tk.Tk()
    root.title("Student Registration")
    root.configure(bg="#DDDDDD")
    root.geometry("600x650") 
    root.resizable(False, False) 

    app = StudentInformationSystemGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
