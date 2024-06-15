# dia.py - script for a dia show. Takes a directory as parameter, opens image files randomly searching from this path, also in sub-directories. The images are scrolled from left to right

import os
import random
import sys
import threading
from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from screeninfo import get_monitors

class ImageDisplayApp:
    def __init__(self, root, image_dir, monitor_index, reverse):
        self.root = root
        self.image_dir = image_dir
        self.reverse = reverse
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.stop_event = threading.Event()
        self.current_images = []

        # Initialize monitor
        monitors = get_monitors()
        print(monitors)
        if monitor_index is not None and 0 <= monitor_index < len(monitors):
            self.monitor = monitors[monitor_index]
        else:
            self.monitor = monitors[0]  # Default to primary monitor

        self.root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.scroll_images()

    def exit_fullscreen(self, event=None):
        self.root.overrideredirect(False)
        self.stop_event.set()
        self.root.destroy()

    def get_random_image_path(self):
        all_files = []
        for dirpath, _, filenames in os.walk(self.image_dir):
            suitable_files = [os.path.join(dirpath, file) for file in filenames if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            all_files.extend(suitable_files)
        if all_files:
            return random.choice(all_files)
        return None

    def load_image(self, image_path):
        try:
            image = Image.open(image_path)
            screen_width, screen_height = self.monitor.width, self.monitor.height
            image.thumbnail((screen_width, screen_height), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except (OSError, UnidentifiedImageError) as e:
            print(f"Error loading image {image_path}: {e}")
            return None

    def scroll_images(self):
        direction = -5 if not self.reverse else 5
        for img, item_id in self.current_images:
            self.canvas.move(item_id, direction, 0)
        
        # Remove images that have moved out of the canvas
        if self.reverse:
            self.current_images = [(img, item_id) for img, item_id in self.current_images if self.canvas.coords(item_id)[0] - img.width() // 2 < self.monitor.width]
        else:
            self.current_images = [(img, item_id) for img, item_id in self.current_images if self.canvas.coords(item_id)[0] + img.width() // 2 > 0]

        # Check if we need to add a new image
        if self.reverse:
            if not self.current_images or self.canvas.coords(self.current_images[-1][1])[0] > self.current_images[-1][0].width() // 2:
                self.add_new_image()
        else:
            if not self.current_images or self.canvas.coords(self.current_images[-1][1])[0] < self.monitor.width - self.current_images[-1][0].width() // 2:
                self.add_new_image()

        if not self.stop_event.is_set():
            self.root.after(50, self.scroll_images)

    def add_new_image(self):
        while True:
            image_path = self.get_random_image_path()
            if image_path:
                image_tk = self.load_image(image_path)
                if image_tk:
                    img_width = image_tk.width()
                    img_height = image_tk.height()
                    screen_width = self.monitor.width
                    screen_height = self.monitor.height
                    x_position = screen_width + img_width // 2 if not self.reverse else -img_width // 2
                    item_id = self.canvas.create_image(x_position, screen_height // 2, anchor=tk.CENTER, image=image_tk)
                    self.current_images.append((image_tk, item_id))
                    self.canvas.image = image_tk  # Keep a reference to avoid garbage collection
                    break

def main(image_dir, monitor_index, reverse):
    root = tk.Tk()
    app = ImageDisplayApp(root, image_dir, monitor_index, reverse)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dia.py <directory_path> [-m <monitor_index>] [-r]")
        sys.exit(1)
    
    image_directory = sys.argv[1]
    monitor_index = None
    reverse = False

    if '-m' in sys.argv:
        monitor_index = int(sys.argv[sys.argv.index('-m') + 1])
    
    if '-r' in sys.argv:
        reverse = True

    if not os.path.isdir(image_directory):
        print("The provided path is not a directory.")
        sys.exit(1)
    
    main(image_directory, monitor_index, reverse)
