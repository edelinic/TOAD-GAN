import tkinter as tk
import torch
from PIL import Image, ImageTk
from utils.level_image_gen import LevelImageGen
import os
import numpy as np

colour_map = {
    '-': '#FFFFFF',  # White for dashes
    'g': '#00FF00',  # Green for 'g'
    'S': '#FFFF00',  # Yellow for 'S'
    '@': '#FF00FF',  # Magenta for '@'
    '!': '#FF0000',  # Red for '!'
    'C': '#0000FF',  # Blue for 'C'
    'U': '#00FFFF',  # Cyan for 'U'
    't': '#FFA500',  # Orange for 't'
    '#': '#808080',  # Gray for '#'
    'X': '#000000',  # Black for 'X'
    'o': '#8B4513'   # Brown for Path (added token)
}
            
class LevelEditorApp:
    def __init__(self, root, ):
        self.root = root
        self.root.title("Pixel Art App")

        # Define pixel grid dimensions
        self.grid_width = 202
        self.grid_height = 16
        self.pixel_size = 16  # Size of each pixel in the canvas
        
        # Initialize the grid representation
        self.grid_representation = [['-' for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Create a frame to hold the canvas and scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        self.canvas = tk.Canvas(self.frame, width=self.grid_width * self.pixel_size, height=self.grid_height * self.pixel_size, bg='white')
        self.canvas.pack(side=tk.TOP)

        # Draw the grid
        self.draw_grid()

        # Bind mouse events for painting
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)

        # Set up colour
        self.colour = 'black'

        # Load the predefined level
        self.load_level()
        
        # Add horizontal scrollbar
        self.h_scrollbar = tk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Add export button
        self.export_button = tk.Button(root, text="Export to TXT", command=self.export_to_txt)
        self.export_button.pack(side=tk.BOTTOM)

    def draw_grid(self):
        """Draw the grid on the canvas."""
        for x in range(0, self.grid_width * self.pixel_size, self.pixel_size):
            self.canvas.create_line(x, 0, x, self.grid_height * self.pixel_size, fill='gray', tags='grid')
        for y in range(0, self.grid_height * self.pixel_size, self.pixel_size):
            self.canvas.create_line(0, y, self.grid_width * self.pixel_size, y, fill='gray', tags='grid')

    def paint(self, event):
            """Handle the painting on the canvas, accounting for scroll position."""
            # Get the current scroll position
            scroll_x = self.canvas.xview()[0] * self.grid_width * self.pixel_size
            scroll_y = self.canvas.yview()[0] * self.grid_height * self.pixel_size

            # Adjust the event coordinates by subtracting the scroll offsets
            x = (event.x + scroll_x) // self.pixel_size * self.pixel_size
            y = (event.y + scroll_y) // self.pixel_size * self.pixel_size

            # Ensure the coordinates are within bounds
            col_index = int(x // self.pixel_size)
            row_index = int(y // self.pixel_size)
            
            if 0 <= col_index < self.grid_width and 0 <= row_index < self.grid_height:
                # Place the image token
                img = token_img_dict.get(self.current_token)
                if img:
                    self.canvas.create_image(x, y, anchor='nw', image=img)

                    # Update the grid representation
                    self.grid_representation[row_index][col_index] = self.current_token

    def set_colour(self, colour):
        """Set the current colour."""
        self.colour = colour
    
    def set_current_token(self, token):
        """Set the current token. Alternative to set colour"""
        self.current_token = token

    def fill_colour_from_image(self, image):
        """Return the average RGB colour from the image."""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image_array = np.array(image)
        
        # Compute the average colour
        average_colour = image_array.mean(axis=(0, 1))
        
        return tuple(average_colour.astype(int))

    def load_level(self):
        """Load the predefined level and fill the canvas accordingly."""
        with open('exported_level.txt', 'r') as file:
            content = file.read()

            # Remove leading/trailing whitespace and split into lines
            rows = content.strip().split('\n')

            for row_index, row in enumerate(content.strip().split('\n')):
                for col_index, char in enumerate(row):
                    # Get the image corresponding to the character
                    img = token_img_dict.get(char)
                    if img:
                        # Place the image on the canvas
                        x1 = col_index * self.pixel_size
                        y1 = row_index * self.pixel_size
                        self.canvas.create_image(x1, y1, anchor='nw', image=img)
                        
                        self.grid_representation[row_index][col_index] = char
                        
    def export_to_txt(self):
        """Export the current representation of the canvas to a text file."""
        with open('exported_level.txt', 'w') as f:
            for row in self.grid_representation:
                f.write(''.join(row) + '\n')

# Create the main window
root = tk.Tk()

# Add a simple colour picker
colour_frame = tk.Frame(root)
colour_frame.pack()

ImgGen = LevelImageGen(os.path.join(os.path.join(os.curdir, "utils"), "sprites"))
# Token dictionary 
full_token_list = torch.load("files/token_list.pth")
token_img_dict = {
    token: ImageTk.PhotoImage(ImgGen.render([token]))
    for token in full_token_list
}

app = LevelEditorApp(root)

for token,colour in colour_map.items():
    button = tk.Button(colour_frame, image=token_img_dict[token], bg=colour, width=50, height=50,
                       command=lambda t=token: app.set_current_token(t)) 
    button.image = token_img_dict[token]
    button.pack(side=tk.LEFT)

root.mainloop()
