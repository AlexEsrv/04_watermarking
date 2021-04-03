from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from pathlib import Path


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Watermarking App')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.upper_menu_frame = tk.Frame(self)
        self.upper_menu_frame.grid(row=0, column=0, padx=5, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.upper_menu_frame.columnconfigure(0, weight=1)
        self.upper_menu_frame.columnconfigure(1, weight=1)
        self.upper_menu_frame.columnconfigure(2, weight=1)

        self.button_open = tk.Button(self.upper_menu_frame, text='Open', command=self.open_file)
        self.button_open.grid(row=0, column=0, padx=10, sticky=(tk.W, tk.E))

        self.button_save = tk.Button(self.upper_menu_frame, text='Save', command=self.save_file)
        self.button_save.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))

        self.add_watermark = tk.Button(self.upper_menu_frame, text='Add', command=self.add_watermark)
        self.add_watermark.grid(row=0, column=2, padx=10, sticky=(tk.W, tk.E))

        self.canvas = tk.Canvas(self)
        self.canvas.config(width=400, height=400)
        self.canvas.grid(row=1, column=0)
        self.canvas.tag_bind("movable", "<Button-1>", self.start_moving)
        self.canvas.tag_bind("movable", "<ButtonRelease-1>", self.stop_moving)
        self.canvas.tag_bind("movable", "<B1-Motion>", self.move)

        self.w_add = None
        self.entry_wtr = None
        self.font_wtr = None
        self.image = None
        self.image_path = ''
        self.photo_image = None
        self.canvas_image = None
        self.watermark_text = ''
        self.watermark_text_object = None
        self.color = None
        self.font_size = 0
        self.text_color = "#FFFFFF"

        self.object_to_drag = None
        self.object_x = 0
        self.object_y = 0

    def open_file(self):
        file_types = (('jpeg', '*.jpg'), ('png', '*.png'))
        self.image_path = filedialog.askopenfilename(title='Open file', initialdir='./', filetypes=file_types)
        if self.image_path != '':
            self.image = Image.open(self.image_path)
            self.photo_image = PhotoImage(self.image)
            self.canvas.config(width=self.image.size[0]+6, height=self.image.size[1]+6)
            self.canvas_image = self.canvas.create_image(3, 3, anchor='nw', image=self.photo_image)

    def save_file(self):
        if self.image is not None:
            font = ImageFont.truetype(font="arial.ttf", size=self.font_size)
            draw = ImageDraw.Draw(self.image)
            draw.text(tuple(self.canvas.coords(self.watermark_text_object)), text=self.watermark_text, font=font, fill=self.text_color)
            path = Path(self.image_path)
            new_path = path.parent.joinpath('w_' + path.name)
            self.image.save(new_path)

    def add_watermark(self):
        self.w_add = tk.Toplevel(self)
        self.w_add.title('Add watermark')
        w_frame_upper = tk.Frame(self.w_add)
        w_frame_upper.grid(row=0, column=0)
        label_wtr = tk.Label(w_frame_upper, text='Watermark text:')
        label_wtr.grid(row=0, column=0, padx=5, pady=5)
        self.entry_wtr = tk.Entry(w_frame_upper)
        self.entry_wtr.grid(row=0, column=1, padx=5, pady=5)

        font_wtr_label = tk.Label(w_frame_upper, text='Font size:')
        font_wtr_label.grid(row=1, column=0, padx=5, pady=5)
        self.font_wtr = tk.Entry(w_frame_upper)
        self.font_wtr.grid(row=1, column=1, padx=5, pady=5)

        color_button = tk.Button(w_frame_upper, text='Color', command=self.choose_color)
        color_button.grid(row=2, column=0)

        ok_button = tk.Button(self.w_add, text='OK', command=self.add_watermark_close)
        ok_button.grid(row=1, column=0, pady=[0, 10])

        self.w_add.resizable(False, False)
        self.w_add.grab_set()
        self.w_add.wait_window()

    def add_watermark_close(self):
        f_size = self.font_wtr.get()
        self.watermark_text = self.entry_wtr.get()

        if not f_size.isdigit():
            self.font_size = 14
        elif int(f_size) == 0:
            self.font_size = 14
        else:
            self.font_size = int(f_size)

        if self.watermark_text != "":
            if self.color is not None:
                self.text_color = self.color[1]
            else:
                self.text_color = "#FFFFFF"

            self.watermark_text_object = self.canvas.create_text(100, 100, text=self.watermark_text, fill=self.text_color, font=('Arial', self.font_size), tags=("movable"), anchor="nw")
        else:
            self.canvas.delete(self.watermark_text_object)
            self.watermark_text_object = None

        self.w_add.destroy()

    def choose_color(self):
        color_dialog = colorchooser.Chooser(self.w_add)
        self.color = color_dialog.show()

    def start_moving(self, event):
        self.object_to_drag = self.canvas.find_closest(event.x, event.y)[0]
        self.object_x = event.x
        self.object_y = event.y

    def stop_moving(self, event):
        self.object_to_drag = None
        self.object_x = 0
        self.object_y = 0

    def move(self, event):
        delta_x = event.x - self.object_x
        delta_y = event.y - self.object_y
        self.canvas.move(self.object_to_drag, delta_x, delta_y)
        self.object_x = event.x
        self.object_y = event.y


if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()