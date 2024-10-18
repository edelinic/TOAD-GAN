import tkinter as tk
import torch
from PIL import Image, ImageTk
from utils.level_image_gen import LevelImageGen
import os
import torch 
import numpy as np

class PixelArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art App")

        # Define pixel grid dimensions
        self.grid_width = 202
        self.grid_height = 16
        self.pixel_size = 20  # Size of each pixel in the canvas

        # Create a canvas
        self.canvas = tk.Canvas(root, width=self.grid_width * self.pixel_size, height=self.grid_height * self.pixel_size, bg='white')
        self.canvas.pack()

        # Draw the grid
        self.draw_grid()

        # Bind mouse events for painting
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Set up color
        self.color = 'black'

    def draw_grid(self):
        """Draw the grid on the canvas."""
        for x in range(0, self.grid_width * self.pixel_size, self.pixel_size):
            self.canvas.create_line(x, 0, x, self.grid_height * self.pixel_size, fill='gray', tags='grid')
        for y in range(0, self.grid_height * self.pixel_size, self.pixel_size):
            self.canvas.create_line(0, y, self.grid_width * self.pixel_size, y, fill='gray', tags='grid')

    def paint(self, event):
        """Handle the painting on the canvas."""
        x = (event.x // self.pixel_size) * self.pixel_size
        y = (event.y // self.pixel_size) * self.pixel_size

        # Draw a rectangle (pixel) on the canvas
        self.canvas.create_rectangle(x, y, x + self.pixel_size, y + self.pixel_size, fill=self.color, outline='black')

    def set_color(self, color):
        """Set the current color."""
        self.color = color
        
    def fill_color_from_image(self, image):
        """takes an image and returns an RBG color that is the overall colour from that image"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_array = np.array(image)
        
        # Compute the average color
        average_color = image_array.mean(axis=(0, 1))
        
        # Return the average color as an RGB tuple
        return tuple(average_color.astype(int))

# Create the main window
root = tk.Tk()
app = PixelArtApp(root)

# Add a simple color picker
color_frame = tk.Frame(root)
color_frame.pack()

colors = ['black', 'red', 'green', 'blue', 'yellow', 'purple']

ImgGen = LevelImageGen(os.path.join(os.path.join(os.curdir, "utils"), "sprites"))
#token dictionary 
full_token_list = torch.load("files/token_list.pth")
token_img_dict = {
    token: ImageTk.PhotoImage(ImgGen.render([token]))
    for token in full_token_list
}

for color in colors:
    button = tk.Button(color_frame, image=token_img_dict['X'], bg=color, width=50, height=50, command=lambda c=color: app.set_color(c) )
    button.image = token_img_dict['X']
    button.pack(side=tk.LEFT)

root.mainloop()