import tkinter as tk
from tkintermapview import TkinterMapView

class ListPage:
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
        self.gmaps.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.gmaps.set_zoom(4)
        self.gmaps.pack(fill="x", expand=True)

        button_search_frame = tk.Frame(self.root)
        button_search_frame.pack(pady=10)

        self.search_entry = tk.Entry(button_search_frame, font=("Noteworthy", 20), fg="gray")
        self.search_entry.insert(0, "Enter a National Park")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)
        self.search_button = tk.Button(button_search_frame, text="Search", command=lambda: self.search(self.search_entry), font=("Noteworthy", 18))
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.marker_text = tk.Entry(button_search_frame, font=("Noteworthy", 20), fg="gray")
        self.marker_text.insert(0, "National Park Name")
        self.marker_text.bind("<FocusIn>", self.clear)
        self.marker_text.bind("<FocusOut>", self.add)
        self.marker_text.grid(row=0, column=2, padx=5, pady=5)
        self.marker_button = tk.Button(button_search_frame, text="Update", command=lambda: self.change_marker(self.marker_text), font=("Noteworthy", 18))
        self.marker_button.grid(row=0, column=3, padx=5, pady=5)

        self.gmaps.add_right_click_menu_command(label="Add Marker", command=self.add_marker, pass_coords=True)

        self.marker = None

    def search(self, entry):
        search_text = entry.get()
        if search_text and search_text != "Enter a National Park":
            self.gmaps.set_address(search_text)
        entry.delete(0, tk.END)
        self.root.after(100, self.check_focus())

    def check_focus(self):
        if self.root.focus_get() != self.search_entry:
            self.add_placeholder(None)

    def add_marker(self, coords):
        print("Add marker: ", coords)
        new_marker = self.gmaps.set_marker(coords[0], coords[1], text="National Park")
        self.marker = new_marker

    def change_marker(self, marker, new_text):
        if marker:
            marker.set_text(new_text)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter a National Park":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def clear(self, event):
        if self.marker_text.get() == "National Park Name":
            self.marker_text.delete(0, tk.END)
            self.marker_text.config(fg="black")

    def add_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter a National Park")
            self.search_entry.config(fg="gray")

    def add(self, event):
        if not self.marker_text.get():
            self.marker_text.insert(0, "National Park Name")
            self.marker_text.config(fg="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
