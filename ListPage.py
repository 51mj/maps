import tkinter as tk
from tkinter import ttk, messagebox

class Park:
    def __init__(self, name, latitude, longitude, last_visited):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.last_visited = last_visited

    def __str__(self):
        return f"{self.name}"


class ListPage(tk.Frame):
    def __init__(self, root, db, refresh_map_callback):
        super().__init__(root)
        self.root = root
        self.db = db
        self.refresh_map_callback = refresh_map_callback
        self.root.title("Park List")
        self.root.geometry("1250x700")
        self.root.configure(bg="gray")
        self.pack(fill="both", expand=True)

        # Initialize editing
        self.is_editing = False
        self.current_edit_index = None
        self.original_items = []

        # Title Label
        label = tk.Label(root, text="Parks", font=("Arial", 24), bg="gray", fg="white")
        label.pack(pady=10)

        # Frame for the entry fields
        frame1 = tk.Frame(root, bg="gray")
        self.create_form_fields(frame1)
        frame1.pack(padx=20, pady=20, expand=True, fill="both")

        # Frame for buttons
        frame2 = tk.Frame(root, bg="gray")
        self.create_buttons(frame2)
        frame2.pack(pady=10)

        # Treeview to display the parks as a table
        columns = ('Name','Latitude', 'Longitude', 'Last Visited')
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Store parks in a list
        self.parks = []

        self.load_saved_data()

    def create_form_fields(self, frame):
        self.label = tk.Label(frame, text="Name", font=("Arial", 12), bg="gray")
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.last_label = tk.Label(frame, text="Last Visited", font=("Arial", 12), bg="gray")
        self.last_label.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        self.name_entry = tk.Entry(frame, width=100)
        self.name_entry.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.last_visited_entry = tk.Entry(frame, width=100)
        self.last_visited_entry.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

    def create_buttons(self, frame):
        self.edit_button = tk.Button(frame, text="Edit Selected Park", command=self.edit_park, bg="#4682B4")
        self.edit_button.grid(row=0, column=1, padx=10)
        self.delete_button = tk.Button(frame, text="Delete Selected Park", command=self.delete_selected_park, bg="#4682B4")
        self.delete_button.grid(row=0, column=2, padx=10)

        self.search_button = tk.Button(frame, text="Search", command=self.search_parks, bg="#4682B4")
        self.search_button.grid(row=0, column=3, padx=10)

    def edit_park(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a park to edit.")
            return

        for item in selected_item:
            index = self.tree.index(item)
            park_name = self.tree.item(item, "values")[0]
            last_visited = self.tree.item(item, "values")[3]

            # Fill in the entry fields with the selected park's data
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, park_name)
            self.last_visited_entry.delete(0, tk.END)
            self.last_visited_entry.insert(0, last_visited)

            self.current_edit_index = index
            self.is_editing = True

            # Change the edit button to submit button
            self.edit_button.config(text="Submit Changes", command=self.submit_edit)

    def submit_edit(self):
        if self.is_editing:
            park_name = self.name_entry.get().strip()
            last_visited = self.last_visited_entry.get().strip()

            if not park_name or not last_visited:
                messagebox.showwarning("Input Error", "Please provide both Name and Last Visited fields.")
                return

            # Update treeview
            self.tree.item(self.tree.selection(), values=(park_name, last_visited))

            # Update park object and Firestore
            park_to_update = self.parks[self.current_edit_index]
            park_to_update.name = park_name
            park_to_update.last_visited = last_visited  # Update last visited field

            try:
                parks_ref = self.db.collection("NationalParks")
                docs = parks_ref.where("name", "==", park_to_update.name).stream()

                for doc in docs:
                    doc.reference.update({
                        "name": park_name,
                        "last_visited": last_visited
                    })
                    break
            except Exception as e:
                messagebox.showerror("Error", f"Error updating Firestore: {str(e)}")
                return

            # Reset form
            self.name_entry.delete(0, tk.END)
            self.last_visited_entry.delete(0, tk.END)

            # Reset button back to 'Edit Selected Park'
            self.edit_button.config(text="Edit Selected Park", command=self.edit_park)

            # Reload the data to reflect changes
            self.load_saved_data()

            self.is_editing = False

    def delete_selected_park(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a park to delete.")
            return

        for item in selected_item:
            index = self.tree.index(item)
            park_name = self.tree.item(item, "values")[0]

            try:
                parks_ref = self.db.collection("NationalParks")
                docs = parks_ref.where("name", "==", park_name).stream()

                for doc in docs:
                    doc.reference.delete()
                    break

            except Exception as e:
                messagebox.showerror("Error", f"Error deleting from Firestore: {str(e)}")
                return

            self.tree.delete(item)
            del self.parks[index]

        self.refresh_map_callback()

    def load_saved_data(self):
        try:
            parks_ref = self.db.collection("NationalParks")
            docs = parks_ref.stream()

            self.tree.delete(*self.tree.get_children())  # Clear current list
            self.parks = []  # Clear existing park list

            for doc in docs:
                park_data = doc.to_dict()
                name = park_data.get("name", "Unnamed Park")
                latitude = park_data.get("latitude", "Unknown Latitude")
                longitude = park_data.get("longitude", "Unknown Longitude")
                last_visited = park_data.get("last_visited", "Never")
                park = Park(name, latitude, longitude, last_visited)
                self.parks.append(park)
                self.tree.insert('', tk.END, values=(park.name,park.latitude,park.longitude,park.last_visited))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading data from Firestore: {str(e)}")

    def search_parks(self):
        search_term = self.name_entry.get().strip().lower()

        # If search term is empty, reload the original tree with all parks
        if not search_term:
            self.tree.delete(*self.tree.get_children())  # Clear the tree
            for park in self.parks:  # Insert the original list of parks back into the tree
                self.tree.insert('', tk.END, values=(park.name, park.latitude, park.longitude, park.last_visited))
            return  # Exit the function after reloading the original parks

        # Proceed with searching if there's a term
        self.tree.delete(*self.tree.get_children())
        results = [park for park in self.parks if search_term in park.name.lower()]

        for park in results:
            self.tree.insert('', tk.END, values=(park.name, park.latitude, park.longitude, park.last_visited))

        if not results:
            messagebox.showinfo("No Results", "No parks matched your search.")


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = ListPage(root)
    root.mainloop()

