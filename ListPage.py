import tkinter as tk
from tkinter import ttk, messagebox
import os

DEFAULT_FILE_PATH = "park_data.txt"


class Park:
    def __init__(self, name):
        self.name = name


    def __str__(self):
        return f"{self.name} | {self.year}"

class ListPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Park List")
        self.root.geometry("1250x700")

        # Initialize editing
        self.is_editing = False
        self.current_edit_index = None
        self.original_items = []

        # Title Label
        label = tk.Label(root, text="Parks", font=("Arial", 24))
        label.pack(pady=10)

        # Frame for the entry fields
        frame1 = tk.Frame(root)
        self.create_form_fields(frame1)
        frame1.pack(padx=20, pady=20, expand=True, fill="both")

        # Treeview to display the videos as a table
        columns = ('Name')
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=150)

        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Store videos in a list
        self.parks = []

        # Automatically open the file dialog after window initialization
        self.root.after(100, self.open_file)

    def create_form_fields(self, frame):
        labels = ["Video Name", "Year", "Director", "Rating", "Genre"]
        entries = []
        for idx, label_text in enumerate(labels):
            label = tk.Label(frame, text=label_text, font=("Arial", 12))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="nsew")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=1, column=idx, padx=10, pady=5, sticky="nsew")
            entries.append(entry)

        self.video, self.year, self.director, self.rating, self.genre = entries
        for col in range(5):
            frame.grid_columnconfigure(col, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def open_file(self):
        if os.path.exists(DEFAULT_FILE_PATH):
            self.tree.delete(*self.tree.get_children())
            self.videos = []

            with open(DEFAULT_FILE_PATH, 'r') as file:
                for line in file:
                    video_info = line.strip().split(" | ")
                    if len(video_info) == 6:
                        video = Video(video_info[0], video_info[1], video_info[2],
                                      video_info[3], video_info[4], video_info[5])
                        self.videos.append(video)
                        self.tree.insert('', tk.END, values=(video.name, video.year, video.director,
                                                             video.rating, video.genre, video.rental_status))

    def save_park(self):
        try:
            with open(DEFAULT_FILE_PATH, 'w') as file:
                for video in self.videos:
                    file.write(str(video) + "\n")
                messagebox.showinfo("Save Successful", "The video data has been saved!")
                
            self.root.lift()
            self.root.focus_force()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {str(e)}")

    def update_file(self):
        try:
            with open(DEFAULT_FILE_PATH, 'w') as file:
                for video in self.videos:
                    file.write(str(video) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating file: {str(e)}")

    def search_videos(self):
        search_term = self.search.get().strip().lower()

        self.tree.delete(*self.tree.get_children())
        self.root.update()

        results = [video for video in self.videos if (
                search_term in video.name.lower() or
                search_term in video.year.lower() or
                search_term in video.director.lower() or
                search_term in video.rating.lower() or
                search_term in video.genre.lower()
        )]

        for video in results:
            self.tree.insert('', tk.END, values=(video.name, video.year, video.director,
                                                 video.rating, video.genre, video.rental_status))
        self.root.update()
        if not results:
            messagebox.showinfo("No Results", "No videos matched your search.")

    def clear_fields(self):
        self.video.delete(0, tk.END)
        self.year.delete(0, tk.END)
        self.director.delete(0, tk.END)
        self.rating.delete(0, tk.END)
        self.genre.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-topmost", True)
    app = ListPage(root)
    root.mainloop()
