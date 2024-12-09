# scrolling functionality example
from tkinter import Tk, Canvas, Frame, Label, Scrollbar, PhotoImage, Button
from tkinter.constants import BOTH, RIGHT, LEFT, Y

class PaletteApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Image Colour Palette Generator")
        self.window.geometry("800x1000")  # Set the window size

        # Create a canvas and a scrollbar
        self.canvas = Canvas(self.window, bg="black")
        self.scrollbar = Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="black")  # Frame for the scrollable content

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Layout the canvas and scrollbar
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Add your content to the scrollable frame
        self.add_widgets()

        self.window.mainloop()

    def add_widgets(self):
        # Add a title
        title = Label(self.scrollable_frame, text="Image Colour Palette Generator", font=("Arial", 20, "bold"), fg="white", bg="black")
        title.pack(pady=10)

        # Example color palette
        palette_colors = ['#14262a', '#c9a98f', '#7e5f4b', '#ddd3ca', '#a0785d', '#59473a', '#b09275']

        # Add color blocks and hex codes
        for color in palette_colors:
            frame = Frame(self.scrollable_frame, bg=color, height=50, width=200)
            frame.pack(pady=5, padx=10)
            hex_label = Label(frame, text=color, font=("Arial", 12, "bold"), fg="white", bg=color)
            hex_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add a button (e.g., Upload Image button)
        upload_button = Button(self.scrollable_frame, text="Upload Image", font=("Arial", 14), bg="white", command=self.upload_image)
        upload_button.pack(pady=10)

    def upload_image(self):
        print("Upload button clicked!")  # Placeholder for your image upload functionality


# Run the application
if __name__ == "__main__":
    app = PaletteApp()
