#pipinstall

import googlemaps
import tkinter as tk
import subprocess

from tkintermapview import TkinterMapView

gmaps = googlemaps.Client(key = 'AIzaSyALFItD1OlN0HdfJ1hEo3NJEyMR1SrgJto')

class LocationHomepage:
    def __init__(self, root):
        self.root = root
        self.root.title("Map App")
        self.root.geometry("1000x500")

        title_frame = tk.Frame(self.root, height=40)
        title_frame.grid_propagate(False)
        title_frame.grid(sticky="ew")

                
        title_label = tk.Label(title_frame, text="National Park App", bg="gray", font=("Noteworthy", 36))
        title_label.pack(pady=5)

        map_widget = TkinterMapView(root, width=600, height=400, corner_radius=0)
        map_widget.grid(sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
