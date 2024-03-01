import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class CourseInformationSystemGUI:
    def __init__(self, root):
        self.root = root

        self.create_title_label()

    def create_title_label(self):
        title_label = tk.Label(
            self.root,
            text="COURSE REGISTRATION",
            font=("Arial", 25, "bold"),
            relief=tk.GROOVE,
            bd=5,
            bg="#2E2D2D",
            fg="white",
            padx=75
        )
        title_label.grid(row=0, column=0, columnspan=1, sticky='ew')

        self.csv_filename = "courses.csv"
        self.fields = ["courseCode", "courseTitle"]

        # Labels and Entry fields
        self.labels = ["Course Code", "Course Title"]
        self.entries = {label: tk.Entry(self.root, font=("Arial", 14,), bg="white", fg="black") for label in self.labels}

        self.tosearch_label = tk.Label(self.root, text="To Search for Course Information:", font=("Arial", 14, "bold"), bg="#DDDDDD", fg="black")
        self.tosearch_label.place(x=25, y=280)

        self.search_label = tk.Label(self.root, text="Enter Course Code:", font=("Arial", 14), bg="#DDDDDD", fg="black")
        self.search_label.place(x=65, y=310)

        # Place labels and entry fields on the GUI
        x_label_position = 25
        x_entry_position = 175
        y_start_position = 70
        y_increment = 50
        entry_width = 330

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(
                self.root, text=label, font=("Arial", 14, "bold"), bg="#DDDDDD", fg="black"
            )
            label_widget.place(x=x_label_position, y=y_start_position + i * y_increment)

            entry_widget = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
            entry_widget.place(x=x_entry_position, y=y_start_position + i * y_increment, width=entry_width)
            self.entries[label] = entry_widget

#----------------------------------------------------- BUTTONS --------------------------------------------------------
            
        # Add Student button
        self.add_button = tk.Button(self.root, text="ADD", font=("Arial", 13, "bold"), command=self.add_course)
        self.add_button.place(x=120, y=180, width=125)

        # Edit and Save buttons
        self.edit_button = tk.Button(self.root, text="EDIT", font=("Arial", 13, "bold"), command=self.edit_course)
        self.edit_button.place(x=310, y=180, width=125)

        self.save_button = tk.Button(self.root, text="SAVE", font=("Arial", 13, "bold"), command=self.save_changes)
        self.save_button.place(x=310, y=230, width=125)

        # Delete button
        self.delete_button = tk.Button(self.root, text="DELETE", font=("Arial", 13, "bold"), command=self.delete_course)
        self.delete_button.place(x=120, y=230, width=125)

        # Search Entry and Button
        self.search_entry = tk.Entry(self.root, font=("Arial", 14), bg="white", fg="black")
        self.search_entry.place(x=260, y=310, width=100)

        self.search_button = tk.Button(self.root, text="SEARCH", font=("Arial", 13, "bold"), command=self.search_course)
        self.search_button.place(x=380, y=309, width=125)

#--------------------------------------------------------------- TREEVIEW --------------------------------------------------------

        # Create Treeview
        self.tree = ttk.Treeview(self.root, columns=("Course Code","Course Title"), show="headings")

        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Title", text="Course Title")

        self.tree.column("Course Code", width=30)
        self.tree.column("Course Title", width=100)
        self.tree.place(x=25, y=370, width=500, height=200)

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
        for label, value in zip(self.labels, course_values):
            self.entries[label].delete(0, "end")
            self.entries[label].insert(0, value)

    def clear_entry_fields(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

    def save_changes(self):
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select a course to edit.")
            return

        # Retrieve edited values from entry fields
        edited_values = [self.entries[label].get() for label in self.labels]

        selected_course_code = self.tree.item(self.selected_item, "values")[0]

        # Update Treeview with the edited values
        self.tree.item(self.selected_item, values=edited_values)

        # Update CSV file with the edited values
        self.update_csv(selected_course_code, edited_values)

        self.selected_item = None

        self.clear_entry_fields()

    def update_csv(self, selected_course_code, edited_values):
        data = []
        with open(self.csv_filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)

        for row in data:
            if row[0] == selected_course_code:
                row[:] = edited_values
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
        values = [self.entries[label].get() for label in self.labels]

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
        for entry in self.entries.values():
            entry.delete(0, "end")

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

    def search_course(self, event=None):
        keyword = self.search_entry.get().lower()

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
    root.configure(bg="#DDDDDD")
    root.geometry("550x600") 
    root.resizable(False, False) 

    app = CourseInformationSystemGUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
