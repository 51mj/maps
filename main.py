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

        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        entry = tk.Entry(search_frame, font=("Noteworthy", 24))
        entry.grid(row=0, column=0, padx=5, pady=5)
        button = tk.Button(search_frame, text="Search", command=lambda: self.search(entry), font=("Noteworthy", 18))
        button.grid(row=0, column=1, padx=5, pady=5)

    def search(self, entry):
        self.gmaps.set_address(entry.get())
        entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
