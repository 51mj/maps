import tkinter as tk
from tkinter import ttk, messagebox
import os

DEFAULT_FILE_PATH = "park_data.txt"

class Park:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"


class ListPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Park List")
        self.root.geometry("1250x700")
        self.root.configure(bg="#87CEEB")  # Set background color to light blue

        # Initialize editing
        self.is_editing = False
        self.current_edit_index = None
        self.original_items = []

        # Title Label
        label = tk.Label(root, text="Parks", font=("Arial", 24), bg="#87CEEB", fg="white")
        label.pack(pady=10)

        # Frame for the entry fields
        frame1 = tk.Frame(root, bg="#87CEEB")
        self.create_form_fields(frame1)
        frame1.pack(padx=20, pady=20, expand=True, fill="both")

        # Frame for buttons
        frame2 = tk.Frame(root, bg="#87CEEB")
        self.create_buttons(frame2)
        frame2.pack(pady=10)

        # Treeview to display the parks as a table
        columns = ('List',)
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Store parks in a list
        self.parks = []

        # Automatically open the file dialog after window initialization
        self.root.after(100, self.open_file)

    def create_form_fields(self, frame):
        label = tk.Label(frame, text="Name", font=("Arial", 12), bg="#87CEEB", fg="white")
        label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

    def create_buttons(self, frame):
        add_button = tk.Button(frame, text="Add Park", command=self.add_park, bg="#4682B4", fg="white")
        add_button.grid(row=0, column=0, padx=10)

        delete_button = tk.Button(frame, text="Delete Selected Park", command=self.delete_selected_park, bg="#4682B4", fg="white")
        delete_button.grid(row=0, column=1, padx=10)

        search_button = tk.Button(frame, text="Search", command=self.search_parks, bg="#4682B4", fg="white")
        search_button.grid(row=0, column=2, padx=10)

        save_button = tk.Button(frame, text="Save List", command=self.save_parks, bg="#4682B4", fg="white")
        save_button.grid(row=0, column=3, padx=10)

    def add_park(self):
        name = self.name_entry.get().strip()
        if name:
            park = Park(name)
            self.parks.append(park)
            self.tree.insert('', tk.END, values=(park.name,))
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a park name.")

    def delete_selected_park(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a park to delete.")
            return

        for item in selected_item:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.parks[index]

    def open_file(self):
        if os.path.exists(DEFAULT_FILE_PATH):
            self.tree.delete(*self.tree.get_children())
            self.parks = []
            with open(DEFAULT_FILE_PATH, 'r') as file:
                for line in file:
                    name = line.strip()
                    if name:
                        park = Park(name)
                        self.parks.append(park)
                        self.tree.insert('', tk.END, values=(park.name,))

    def save_parks(self):
        try:
            with open(DEFAULT_FILE_PATH, 'w') as file:
                for park in self.parks:
                    file.write(str(park) + "\n")
            messagebox.showinfo("Save Successful", "The park data has been saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def search_parks(self):
        search_term = self.name_entry.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        self.tree.delete(*self.tree.get_children())
        results = [park for park in self.parks if search_term in park.name.lower()]

        for park in results:
            self.tree.insert('', tk.END, values=(park.name,))

        if not results:
            messagebox.showinfo("No Results", "No parks matched your search.")


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = ListPage(root)
    root.mainloop()

