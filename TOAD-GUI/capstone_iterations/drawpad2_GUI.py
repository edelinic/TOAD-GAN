# paint application using Tkinter .....

from tkinter import *
from tkinter.ttk import Scale
from tkinter import  colorchooser,messagebox
from tkinter.filedialog import asksaveasfilename
import PIL.ImageGrab as ImageGrab # pip install pillow
from PIL import Image, ImageTk
color= 'white'
i = 1

from utils.level_image_gen import LevelImageGen
import os
import torch

class Paint():
    def __init__(self,root):
        self.root = root
        self.root.title("Paint")
        self.root.geometry("800x520")
        self.root.configure(background="white")
        self.root.resizable(0,0)

        self.pen_color = "#000000"

        self.color_frame = LabelFrame(self.root,text ="Color",font =('arial',15,'bold'),bd=5,relief=RIDGE,bg='white')
        self.color_frame.place(x=0,y=0,width=70,height=185)

        Colors = ['#ff0000','#ff4dd2','#ffff33','#000000','#0066ff','#660033','#4dff4d','#b300b3','#00ffff','#808080','#99ffcc','#336600','#ff9966','#ff99ff','#00cc99',]
        
        ImgGen = LevelImageGen(os.path.join(os.path.join(os.curdir, "utils"), "sprites"))
        
        full_token_list = torch.load("files/token_list.pth")
        token_img_dict = {}
        for token in full_token_list:
            token_img_dict[token] = ImageTk.PhotoImage(ImgGen.render([token]))
            
        # Create a label to hold the image and place it inside color_frame
        photo = token_img_dict['X']
        image_label = Label(self.color_frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection

        buttons = []
        i=j= 0
        for t in full_token_list:
            button = Button(self.color_frame, image=token_img_dict[t], width=15,bd=2,relief=RIDGE)
            button.image = token_img_dict[t]
            button.grid(row=i,column=j)
            i+=1
            if i== 6:
                i=0
                j=1
        
        self.erase_button = Button(self.root,text="Eraser",bd=4,relief=RIDGE,width=8,command=self.eraser,bg="white")
        self.erase_button.place(x=0,y=187)

        self.clear_sreen_button =Button(self.root,text="Clear",bd=4,relief=RIDGE,width=8,command=lambda : self.canvas.delete("all"),bg="white")
        self.clear_sreen_button.place(x=0,y=217)

        self.save_button =Button(self.root,text="Save",bd=4,relief=RIDGE,width=8,command=self.save_paint,bg="white")
        self.save_button.place(x=0,y=247)

        self.canvas_color_button =Button(self.root,text="Canvas",bd=4,relief=RIDGE,width=8,command=self.canvas_color,bg="white")
        self.canvas_color_button.place(x=0,y=277)

        self.pen_size_scale_frame = LabelFrame(self.root,text="Size",bd=5,relief=RIDGE,bg="white",font =('arial',15,'bold'))
        self.pen_size_scale_frame.place(x=0,y=310,height=200,width=70)

        self.pen_size = Scale(self.pen_size_scale_frame,orient='vertical', from_=50, to=0, command=None,length=170)
        self.pen_size.set(1)
        self.pen_size.grid(row=0,column=1,padx=15)


        self.canvas = Canvas(self.root,bg='white',bd=5,relief='groove',height=160,width=1600)
        self.canvas.place(x=80,y=0)

        # Blind mouse dragging event to canvas
        self.canvas.bind("<B1-Motion>",self.paint)


    def paint(self,event):
        global pen_color
        x1,y1 = ( event.x - 2), ( event.y - 2)
        x2,y2 = (event.x + 2) , ( event.y + 2)
        if(i):
            self.canvas.config(cursor = 'plus')
        self.canvas.create_oval(x1,y1,x2,y2,fill = self.pen_color,outline=self.pen_color,width=self.pen_size.get())

    def select_color(self,col):
        global i
        i = 1
        self.pen_color = col


    def eraser(self):
        global color
        global i
        self.pen_color = color
        self.canvas.config(cursor = 'dot')
        i = 0

    def canvas_color(self):
        global color
        color = colorchooser.askcolor()
        color = color[1]
        self.canvas.config(background=color)

    def save_paint(self):
        try:
            self.canvas.update()
            filename = asksaveasfilename(defaultextension='.jpg')
            print(filename)
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            #print(x)
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            #print(y)
            x1 = x + self.canvas.winfo_width()
            #print(x1)
            y1 = y + self.canvas.winfo_height()
            #print(y1)
            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
            messagebox.showinfo('paint says ','image is saved as '+str(filename))

        except:
            pass


if __name__ == "__main__":
    root = Tk()
    Paint(root)
    root.mainloop()