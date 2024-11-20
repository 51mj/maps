from tkinter import BOTH

import tkinter as tk
from tkintermapview import TkinterMapView
    
class LocationHomepage:
    def __init__(self, root):
        self.root = root
        self.root.title("Map App")
        self.root.geometry("1250x700")

        title_frame = tk.Frame(self.root, height=40)
        title_frame.pack(fill="both", expand=True)


        title_label = tk.Label(title_frame, text="National Park App", bg="gray", font=("Noteworthy", 36))
        title_label.pack(fill="both", expand=True)

        self.gmaps = TkinterMapView(root, width=1000, height=500)
        self.gmaps.set_position(41.5868, -93.6250)
        self.gmaps.set_zoom(4)
        self.gmaps.pack(fill="x", expand=True)

        button_search_frame = tk.Frame(self.root)
        button_search_frame.pack(pady=10)

        search_entry = tk.Entry(button_search_frame, font=("Noteworthy", 20))
        search_entry.grid(row=0, column=0, padx=5, pady=5)
        search_button = tk.Button(button_search_frame, text="Search", command=lambda: self.search(search_entry), font=("Noteworthy", 18))
        search_button.grid(row=0, column=1, padx=5, pady=5)

        self.gmaps.add_right_click_menu_command(label="Add Marker", command=self.add_marker, pass_coords=True)

    def search(self, entry):
        self.gmaps.set_address(entry.get())
        entry.delete(0, tk.END)

    def add_marker(self, coords):
        print("Add marker: ", coords)
        new_marker = self.gmaps.set_marker(coords[0], coords[1], text="New Marker")

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
