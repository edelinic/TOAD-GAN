import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Colored Grid Display")

# Define the content to be displayed
content = """
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
----------------------------------------------------------------------------------g----------------------------------------------------------------------------------------------------------------------- 
----------------------!---------------------------------------------------------SSSSSSSS---SSS!--------------@-----------SSS----S!!S--------------------------------------------------------##------------ 
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------###------------ 
-------------------------------------------------------------------------------g----------------------------------------------------------------------------------------------------------####------------ 
----------------------------------------------------------------1------------------------------------------------------------------------------------------------------------------------#####------------ 
----------------!---S@S!S---------------------tt---------tt------------------S@S--------------C-----SU----!--!--!-----S----------SS------#--#----------##--#------------SS!S------------######------------ 
--------------------------------------tt------tt---------tt-----------------------------------------------------------------------------##--##--------###--##--------------------------#######------------ 
----------------------------tt--------tt------tt---------tt----------------------------------------------------------------------------###--###------####--###-----tt--------------tt-########--------F--- 
---M-----------------g------tt--------tt-g----tt-----g-g-tt------------------------------------g-g--------k-----------------gg-g-g----####--####----#####--####----tt---------gg---tt#########--------#--- 
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--XXXXXXXXXXXXXXX---XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--XXXXXXXXXXXXXXX---XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

# Define a color mapping for different characters
color_map = {
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
}

# Color to draw with
draw_color = '#FF0000'  # Default draw color
drawing = False  # Track if the mouse is pressed

# Create a frame for the scrollable area
scrollable_frame = tk.Frame(root)
scrollable_frame.pack(fill=tk.BOTH, expand=True)

# Add a canvas to the scrollable frame
canvas = tk.Canvas(scrollable_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add vertical and horizontal scrollbars to the canvas
v_scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
h_scrollbar = tk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Configure the canvas
canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Create a frame inside the canvas to hold the labels
label_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=label_frame, anchor="nw")

def change_color(widget):
    """Change the color of the label."""
    widget.config(bg=draw_color)

def on_press(event):
    """Start drawing on mouse button press."""
    global drawing
    drawing = True
    widget = event.widget
    change_color(widget)

def on_release(event):
    """Stop drawing on mouse button release."""
    global drawing
    drawing = False

def on_drag(event):
    """Change color while dragging the mouse."""
    if drawing:
        widget = event.widget
        change_color(widget)

def update_scroll_region(event=None):
    """Update the scroll region to encompass the label frame."""
    label_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Bind the update_scroll_region function to the frame's configure event
label_frame.bind("<Configure>", update_scroll_region)

# Create labels for each character in the content
for row_index, row in enumerate(content.strip().split('\n')):
    for col_index, char in enumerate(row):
        color = color_map.get(char, '#FFFFFF')  # Default to white if char is not mapped
        label = tk.Label(label_frame, text=' ', bg=color, width=2, height=1)  # Smaller size
        label.grid(row=row_index, column=col_index)
        label.bind("<Button-1>", on_press)  # Bind left mouse click
        label.bind("<ButtonRelease-1>", on_release)  # Bind mouse button release
        label.bind("<B1-Motion>", on_drag)  # Bind mouse drag

# Create a color selection frame
color_frame = tk.Frame(root)
color_frame.pack()

def set_draw_color(color):
    """Set the color used for drawing."""
    global draw_color
    draw_color = color

# Add color buttons
colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FFA500', '#808080', '#FFFFFF', '#000000']
for color in colors:
    btn = tk.Button(color_frame, bg=color, width=4, command=lambda c=color: set_draw_color(c))
    btn.pack(side=tk.LEFT)

# Start the Tkinter main loop
root.mainloop()
