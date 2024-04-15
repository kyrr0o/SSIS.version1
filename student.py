import csv
import tkinter as tk
from tkinter import messagebox, ttk

class StudentInformationSystemGUI:
    def __init__(self, root):
        self.root = root
        self.create_title_label()
        self.load_courses_from_csv() 

    def load_courses_from_csv(self):
        self.course_options = []
        try:
            with open("courses.csv", "r") as course_file:
                csvreader = csv.reader(course_file)
                for row in csvreader:
                    self.course_options.append(row[0])
        except FileNotFoundError:
            print("CSV file not found.")

        # Course dropdown menu
        self.course_label = tk.Label(self.root, text="Course Code", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.course_label.place(x=10, y=340)

        self.selected_course = tk.StringVar(self.root)

        if self.course_options:
            self.selected_course.set(self.course_options[0])
            self.course_dropdown = tk.OptionMenu(self.root, self.selected_course, *self.course_options)
        else:
            self.selected_course.set("None")
            self.course_dropdown = tk.OptionMenu(self.root, self.selected_course, "None")

        self.course_dropdown.config(font=("Arial", 12), bg="white", fg="black")
        self.course_dropdown.place(x=160, y=340, width=250)

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
            font=("Arial", 35, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=89
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        self.csv_filename = "students.csv"
        self.fields = ["idNum", "name", "gender", "course", "yearLevel"]

        # Labels and Entry fields
        self.labels = ["Student ID", "First Name", "Last Name", "Gender", "Year Level"]
        self.entries = {label: tk.Entry(self.root, font=("Arial", 17,), bg="white", fg="black") for label in self.labels}

        self.tosearch_label = tk.Label(self.root, text="To Search for Student Information:", font=("Arial", 17, "bold"), bg="#A6A6A6", fg="black")
        self.tosearch_label.place(x=450, y=90)

        self.search_label = tk.Label(self.root, text="Enter Keyword to Search:", font=("Arial", 17), bg="#A6A6A6", fg="black")
        self.search_label.place(x=450, y=140)

        self.search_entry = tk.Entry(self.root, font=("Arial", 17), bg="white", fg="black")
        self.search_entry.place(x=720, y=140, width=230)

        # Place labels and entry fields on the GUI
        x_label_position = 10
        x_entry_position = 160
        y_start_position = 100
        y_increment = 50
        entry_width = 250

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(
                self.root, text=label, font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black"
            )
            label_widget.place(x=x_label_position, y=y_start_position + i * y_increment)

            entry_widget = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
            entry_widget.place(x=x_entry_position, y=y_start_position + i * y_increment, width=entry_width)
            self.entries[label] = entry_widget

        # Gender dropdown
        self.gender_label = tk.Label(self.root, text="Gender", font=("Arial", 14, "bold"), bg="#A6A6A6", fg="black")
        self.gender_label.place(x=x_label_position, y=y_start_position + 3 * y_increment)

        self.gender_variable = tk.StringVar(self.root)
        self.gender_variable.set("Male")  # Default value
        self.gender_dropdown = tk.OptionMenu(self.root, self.gender_variable, "Male", "Female")
        self.gender_dropdown.config(font=("Arial", 12), bg="white", fg="black")
        self.gender_dropdown.place(x=x_entry_position, y=y_start_position + 3 * y_increment, width=entry_width)

#----------------------------------------------------- BUTTONS --------------------------------------------------------

        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.add_student)
        self.add_button.place(x=50, y=470, width=150)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.delete_student)
        self.delete_button.place(x=50, y=520, width=150)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.edit_student)
        self.edit_button.place(x=250, y=470, width=150)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), bg="#0E3643", fg="white", command=self.save_changes)
        self.save_button.place(x=250, y=520, width=150)

        # Search Button
        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), bg="#5D150D", fg="white", command=self.search_student)
        self.search_button.place(x=960, y=140, width=100)

        # Cancel button
        self.cancel_button = tk.Button(self.root, text="CANCEL", font=("Arial", 13, "bold"), bg="#2E2D2D", fg="white", command=self.cancel_edit)
        self.cancel_button.place(x=100, y=400, width=250)

#--------------------------------------------------------------- TREEVIEW -------------------------------------------------------

        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID Number", "Name", "Gender", "Course", "Year Level"), show="headings", selectmode="extended")

        self.tree.heading("ID Number", text="ID Number", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Gender", text="Gender", anchor=tk.CENTER)
        self.tree.heading("Course", text="Course", anchor=tk.CENTER)
        self.tree.heading("Year Level", text="Year Level", anchor=tk.CENTER)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview.Heading", background="#2E2D2D",  foreground="white", font=("Arial", 12, "bold"))

        self.tree.column("ID Number", width=70)
        self.tree.column("Name", width=150) 
        self.tree.column("Gender", width=50)
        self.tree.column("Course", width=50)
        self.tree.column("Year Level", width=50)
        self.tree.place(x=440, y=200, width=600, height=460)

        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.scrollbar.place(x=1040, y=200, height=460)

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.load_students()

        self.selected_item = None

    def edit_student(self):
        selected_items = self.tree.selection()
        if len(selected_items) != 1:
            messagebox.showwarning("Warning", "Please select only one student to edit.")
            return

        self.selected_item = selected_items[0]

        student_values = self.tree.item(self.selected_item, "values")
        if not student_values:
            messagebox.showwarning("Warning", "Selected item does not contain student information.")
            return

        full_name_parts = student_values[1].rsplit(' ', 1)
        first_name = full_name_parts[0]
        last_name = full_name_parts[1] if len(full_name_parts) > 1 else ''

        self.entries["Student ID"].delete(0, "end")
        self.entries["Student ID"].insert(0, student_values[0])

        self.entries["First Name"].delete(0, "end")
        self.entries["First Name"].insert(0, first_name)

        self.entries["Last Name"].delete(0, "end")
        self.entries["Last Name"].insert(0, last_name)

        self.gender_variable.set(student_values[2])

        self.selected_course.set(student_values[3])

        self.entries["Year Level"].delete(0, "end")
        self.entries["Year Level"].insert(0, student_values[4])

    def cancel_edit(self):
        self.selected_item = None
        self.clear_entry_fields()
        self.gender_variable.set("Male")
        if self.course_options:
            self.selected_course.set(self.course_options[0]) 
        else:
            self.selected_course.set("None") 

    def clear_entry_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return

        edited_values = [
            self.entries["Student ID"].get(),
            f"{self.entries['First Name'].get()} {self.entries['Last Name'].get()}", 
            self.gender_variable.get(),
            self.selected_course.get(), 
            self.entries["Year Level"].get()
        ]

        original_id = self.tree.item(self.selected_item, "values")[0]

        if edited_values[0] != original_id and self.check_IDNo(edited_values[0]):
            messagebox.showerror("Error", f"Student {edited_values[0]} already exists.")
            return

        self.tree.item(self.selected_item, values=edited_values)

        self.selected_item = None

        self.update_student_in_csv(edited_values)

        self.clear_entry_fields()

    def update_student_in_csv(self, edited_values):
        data = []
        with open(self.csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != edited_values[0]:
                    data.append(row)
                else:
                    row[0] = edited_values[0]
                    row[1] = edited_values[1]
                    row[2] = edited_values[2]
                    row[3] = edited_values[3]
                    row[4] = edited_values[4]
                    data.append(row)

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
        course_code = self.selected_course.get()
        gender = self.gender_variable.get()

        if any(value == '' for value in [first_name, last_name, idNo, yr_level, gender]):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if self.check_IDNo(idNo):
            messagebox.showerror("Error", f"Student {idNo} already exists.")
            return

        self.tree.insert("", "end", values=[idNo, f"{first_name} {last_name}", gender, course_code, yr_level])

        with open(self.csv_filename, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([idNo, f"{first_name} {last_name}", gender, course_code, yr_level])

        for entry in self.entries.values():
            entry.delete(0, "end")

        messagebox.showinfo("Success", "Student added successfully!")

    def delete_student(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select student(s) to delete.")
            return

        for item in selected_items:
            student_values = self.tree.item(item, "values")
            if not student_values:
                continue  

            student_id = student_values[0]

            self.tree.delete(item)

            self.delete_student_from_csv(student_id)

        messagebox.showinfo("Success", "Selected student(s) deleted successfully!")

    def delete_student_from_csv(self, student_id):
        data = []
        with open(self.csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] != student_id: 
                    data.append(row)

        with open(self.csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def search_student(self):
        search_key = self.search_entry.get().strip().lower()

        if not search_key:
            messagebox.showwarning("Warning", "Please enter a keyword to search.")
            return

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        first_match_item = None

        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values and any(search_key in value.lower() for value in values):
                self.tree.selection_add(item)
                if not first_match_item:
                    first_match_item = item
            else:
                self.tree.selection_remove(item)

        if first_match_item:
            self.tree.see(first_match_item)



def main():
    root = tk.Tk()
    root.title("Student Registration")
    root.configure(bg="#A6A6A6")
    root.geometry("1070x675") 
    root.resizable(False, False) 

    student_app = StudentInformationSystemGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
