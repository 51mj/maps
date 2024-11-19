from tkinter import BOTH

import googlemaps
import tkinter as tk
from tkintermapview import TkinterMapView

class LocationHomepage:
    def __init__(self, root):
        self.root = root
        self.root.title("Map App")
        self.root.geometry("1000x500")

        title_frame = tk.Frame(self.root, height=40)
        title_frame.pack(fill=BOTH, expand=True)


        title_label = tk.Label(title_frame, text="National Park App", bg="gray", font=("Noteworthy", 36))
        title_label.pack(fill=BOTH, expand=True)

        gmaps = TkinterMapView(root, width=1000, height=500)
        gmaps.set_position(41.5868, -93.6250)
        gmaps.set_zoom(4)
        gmaps.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
