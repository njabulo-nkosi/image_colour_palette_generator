from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from sklearn.cluster import KMeans
import numpy as np


class Interface:

    def __init__(self, window):
        self.window = window
        self.window.title('Image Colour Palette Generator')
        self.window.config(pady=50, padx=50, bg='black')

        self.setup_window()
        self.setup_image()
        self.setup_buttons()

    def setup_window(self):
        self.title = Label(self.window, text='Image Colour Palette Generator\n Palette Generator',
                           font=('Courier', 30, 'bold'), pady=20, padx=20,
                           bg='black',
                           fg='white')
        self.title.grid(column=1, row=0)

    def setup_image(self):
        image = Image.open('Image viewer-bro.png')

        max_size = 600
        image.thumbnail((max_size, max_size - 200), Image.Resampling.LANCZOS)

        self.display_image = ImageTk.PhotoImage(image)

        image_label = Label(self.window, image=self.display_image, bg='black')
        image_label.grid(column=1, row=1, pady=20)

    def setup_buttons(self):

        self.start_button = Button(self.window, text='Upload Image',
                                   font=('Courier', 10, 'bold'), pady=10,
                                   command=self.upload_and_process_image)
        self.start_button.grid(column=1, row=4)

    def upload_and_process_image(self):

        file_path = self.get_local_file()
        if file_path:
            # self.display_uploaded_image(file_path)

            extracted_palette = self.extract_palette(file_path)
            self.display_palette(extracted_palette)
            self.update_image(extracted_palette)

    def get_local_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('Image files', '.*png;*.jpeg;*.jpg')])

        if file_path:
            print(f'File path: {file_path}')

            return file_path

    def is_hex_color(self, color):

        if isinstance(color, str) and len(color) == 7 and color.startswith('#'):
            try:
                int(color[1:], 16)
                return True
            except ValueError:
                return False
        return False

    def extract_palette(self, file_path):

        image = Image.open(file_path).convert('RGB')
        image = image.resize((200, 200))
        data = np.array(image)
        pixels = data.reshape(-1, 3)

        kmeans = KMeans(n_clusters=10, random_state=0).fit(pixels)
        colors = kmeans.cluster_centers_
        hex_colors = ['#%02x%02x%02x' % tuple(map(int, color)) for color in colors]

        valid_colors = [color for color in hex_colors if self.is_hex_color(color)]
        if len(valid_colors) < len(hex_colors):
            print(f'Invalid hex colors found and deleted: {set(hex_colors) - set(valid_colors)}')

        return valid_colors

    def display_palette(self, palette):
        for i, color in enumerate(palette):

            color_label = Label(self.window, text=color, bg=color, width=20, height=2, fg='white' if i % 2 else 'black')
            color_label.grid(row=5 + i, column=1, pady=5)

    def update_image(self, hex_colors):

        print(f"Received colors: {hex_colors}")

        for widget in self.window.grid_slaves():
            if int(widget.grid_info()['row']) == 1:
                widget.destroy()

        palette_canvas = Canvas(self.window, width=600, height=100, bg='white', highlightthickness=1)
        palette_canvas.grid(column=1, row=1, pady=20)

        block_width = 600 // len(hex_colors)

        for i, hex_code in enumerate(hex_colors):
            print(f"Drawing rectangle with color: {hex_code}")
            palette_canvas.create_rectangle(i * block_width, 0, (i + 1) * block_width, 100, fill=hex_code, outline='')

