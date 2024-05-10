import tkinter as tk
from pymongo import MongoClient
import requests
from io import BytesIO
from PIL import Image, ImageTk


class PhotoSliderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Photo Slider")

        # MongoDB connection
        self.client = MongoClient('mongodb+srv://newUser:TXk.ch28bNCds5c@cluster0.ir11p5g.mongodb.net/lostcal')
        self.db = self.client['lostcal']
        self.collection = self.db['lostpepoles']

        # Fetch photo URLs from MongoDB
        self.photo_urls = self.get_photo_urls()
        self.current_photo_index = 0

        # Set up GUI
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

        # Load first photo
        self.load_photo()

        # Start slideshow
        self.start_slideshow()

    def get_photo_urls(self):
        """Fetch photo URLs from MongoDB"""
        photo_urls = []
        for doc in self.collection.find():
            photo_urls.append(doc['img'])
        return photo_urls

    def load_photo(self):
        """Load and display photo from URL"""
        url = self.photo_urls[self.current_photo_index]
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((600, 400))
        photo = ImageTk.PhotoImage(image)

        # Display photo on canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo  # Keep a reference to prevent garbage collection

    def start_slideshow(self):
        """Start the slideshow"""
        self.next_photo()
        self.master.after(100, self.start_slideshow)

    def next_photo(self):
        """Display next photo in the slideshow"""
        self.current_photo_index = (self.current_photo_index + 1) % len(self.photo_urls)
        self.load_photo()


def main():
    root = tk.Tk()
    app = PhotoSliderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
