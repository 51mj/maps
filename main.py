import tkinter as tk
import requests
from tkintermapview import TkinterMapView
import tkinter.simpledialog
from ListPage import ListPage
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"C:\Users\ianni\PycharmProjects\map-bytes.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def reverse_geocode(lat, lon):
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'lat': str(lat),
        'lon': str(lon),
        'format': 'jsonv2',
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'The Bytes (ian.nichols056@gmail.com)'
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def geocode(location_name):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': location_name,
        'format': 'jsonv2',
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'The Bytes (ian.nichols056@gmail.com)'
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

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
        self.gmaps.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.gmaps.set_zoom(4)
        self.gmaps.pack(fill="x", expand=True)

        self.load_saved_data()

        self.display_label = tk.Label(self.root, text="", font=("Noteworthy", 18), fg="black", wraplength=1000)
        self.display_label.pack(pady=10)

        button_search_frame = tk.Frame(self.root)
        button_search_frame.pack(pady=10)

        self.search_entry = tk.Entry(button_search_frame, font=("Noteworthy", 20), fg="gray")
        self.search_entry.insert(0, "Enter a National Park")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)
        self.search_button = tk.Button(button_search_frame, text="Search", command=lambda: self.search(self.search_entry), font=("Noteworthy", 18))
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.list_button = tk.Button(button_search_frame, text="List Page", command=self.open_list, font=("Noteworthy", 18))
        self.list_button.grid(row=0, column=4, padx=5, pady=5)

        self.gmaps.add_right_click_menu_command(label="Add Marker", command=self.add_marker, pass_coords=True)

        self.marker = None

    def load_saved_data(self):
        parks_ref = db.collection("NationalParks")
        docs = parks_ref.stream()

        for doc in docs:
            park_data = doc.to_dict()
            latitude = park_data.get("latitude")
            longitude = park_data.get("longitude")
            name = park_data.get("name", "National Park")

            self.gmaps.set_marker(latitude, longitude, text=name)

    def search(self, entry):
        search_text = entry.get().strip()
        if not search_text or search_text == "Enter a National Park":
            return

        try:
            location_data = geocode(search_text)

            if location_data:
                first_result = location_data[0]
                lat = float(first_result.get("lat"))
                lon = float(first_result.get("lon"))
                display_name = first_result.get("display_name", "Unknown Location")

                self.gmaps.set_position(lat, lon)
                self.gmaps.set_zoom(12)

                self.display_label.config(text=f"Location: {display_name}")
            else:
                print("No results found")
        except Exception as e:
            print(f"Error during search: {e}")

        entry.delete(0, tk.END)
        self.root.after(100, self.check_focus())


    def check_focus(self):
        if self.root.focus_get() != self.search_entry:
            self.add_placeholder(None)

    def add_marker(self, coords):
        park_name = tk.simpledialog.askstring("Park Name", "Enter the name of the National Park:")

        if park_name:
            print("Add marker: ", coords)
            new_marker = self.gmaps.set_marker(coords[0], coords[1], text=park_name)
            self.marker = new_marker

            park_data = {
                "latitude": coords[0],
                "longitude": coords[1],
                "name": park_name,
            }

            doc_ref = db.collection('NationalParks').document(park_name)
            doc_ref.set(park_data)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter a National Park":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter a National Park")
            self.search_entry.config(fg="gray")

    def open_list(self):
        new_window = tk.Toplevel(self.root)
        ListPage(new_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = LocationHomepage(root)
    root.mainloop()
