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
            # ImageDraw.text(xy, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None,
            #                features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False)
            # self.watermark_text_object.
            #
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


# root = tk.Tk()
# root.title('Watermarking App')
#
# def open_file():
#     pass
#
# def save_file():
#     pass
#
# def add_watermark():
#     w_add = tk.Toplevel(root)
#     w_add.title('Add watermark')
#     w_frame_upper = tk.Frame(w_add)
#     w_frame_upper.grid(row=0, column=0)
#     label_wtr = tk.Label(w_frame_upper, text='Watermark text:')
#     label_wtr.grid(row=0, column=0, padx=5, pady=5)
#     entry_wtr = tk.Entry(w_frame_upper)
#     entry_wtr.grid(row=0, column=1, padx=5, pady=5)
#
#     font_wtr = tk.Label(w_frame_upper, text='Font size:')
#     font_wtr.grid(row=1, column=0, padx=5, pady=5)
#     font_wtr = tk.Entry(w_frame_upper)
#     font_wtr.grid(row=1, column=1, padx=5, pady=5)
#
#     color_button = tk.Button(w_frame_upper, text='Color')
#     color_button.grid(row=2, column=0)
#
#     ok_button = tk.Button(w_add, text='OK')
#     ok_button.grid(row=1, column=0, pady=[0, 10])
#
#     w_add.resizable(False, False)
#     w_add.grab_set()
#     w_add.wait_window()
#
#
#
#
#
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(1, weight=1)
#
# upper_menu_frame = tk.Frame(root)
# upper_menu_frame.grid(row=0, column=0, padx=5, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
# upper_menu_frame.columnconfigure(0, weight=1)
# upper_menu_frame.columnconfigure(1, weight=1)
# upper_menu_frame.columnconfigure(2, weight=1)
#
#
# button_open = tk.Button(upper_menu_frame, text='Open', command=open_file)
# button_open.grid(row=0, column=0, padx=10, sticky=(tk.W, tk.E))
#
# button_save = tk.Button(upper_menu_frame, text='Save', command=save_file)
# button_save.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))
#
# add_watermark = tk.Button(upper_menu_frame, text='Add', command=add_watermark)
# add_watermark.grid(row=0, column=2, padx=10, sticky=(tk.W, tk.E))
#
# canvas = tk.Canvas()
# canvas.config(width=400, height=400)
# canvas.grid(row=1, column=0)
#
#
#
#
# root.mainloop()
# image = None
# photo_img = None
# im_path = ''
# canvas_image = None
# #
# # with Image.open(im_path) as im:
# #
# #     draw = ImageDraw.ImageDraw(im)
# #     draw.line([(0, 0), im.size], fill=(85, 232, 62))
# #     draw.line([(0, im.size[1]), (im.size[0], 0)], fill=128)
# #
# #     im.save('e_' + im_path)
#
# # window = tk.Tk()
# # window.title("TEST")
#
#
# def process_image():
#     global photo_img
#
#     draw = ImageDraw.Draw(image)
#     draw.line([(0, 0), (image.size[0], image.size[1])], fill=(85, 232, 62))
#     photo_img = PhotoImage(image)
#     canvas.itemconfig(canvas_image, image=photo_img)
#
#
# def save_image():
#     p = Path(im_path)
#     new_path = p.parent.joinpath('w_' + p.name)
#     image.save(new_path)
#
#
# def open_image():
#     global image, im_path, photo_img, canvas_image
#     file_types = (('jpeg', '*.jpg'), ('png', '*.png'))
#     im_path = filedialog.askopenfilename(title='Open file', initialdir='./', filetypes=file_types)
#     if im_path != '':
#         image = Image.open(im_path)
#         photo_img = PhotoImage(image)
#         canvas.config(width=image.size[0]+6, height=image.size[1]+6)
#         canvas_image = canvas.create_image(3, 3, anchor='nw', image=photo_img)
#
#
# def new_window():
#     w = tk.Toplevel()
#     label = tk.Label(w, text='New window')
#     entry = tk.Entry(w)
#     label.grid(row=0, column=0)
#     entry.grid(row=0, column=1)
#     w.grab_set()
#
# # with Image.open(im_path) as im:
#
# window = tk.Tk()
# window.title("Watermarking")
#
# button_open = tk.Button(text='Open', command=open_image)
# button_open.pack()
#
# button_process = tk.Button(text='Process', command=process_image)
# button_process.pack()
#
# button_save = tk.Button(text='Save', command=save_image)
# button_save.pack()
#
# button_new_window = tk.Button(text='New window', command=new_window)
# button_new_window.pack()
#
# # photo_img = PhotoImage(im)
# # canvas = tk.Canvas(width=im.size[0]+5, height=im.size[1]+5)
# canvas = tk.Canvas()
# canvas.pack()
# window.mainloop()

# object_to_drag = None
# object_x = 0
# object_y = 0
# color = "#000000"
#
# watermark_text_object = None
# watermark_text = ""
#
# def start_moving(event):
#     global object_to_drag, object_x, object_y
#     object_to_drag = canvas.find_closest(event.x, event.y)[0]
#     object_x = event.x
#     object_y = event.y
#
# def stop_moving(event):
#     global object_to_drag, object_x, object_y
#     object_to_drag = None
#     object_x = 0
#     object_y = 0
#
# def move(event):
#     global object_to_drag, object_x, object_y, canvas
#     delta_x = event.x - object_x
#     delta_y = event.y - object_y
#     canvas.move(object_to_drag, delta_x, delta_y)
#     object_x = event.x
#     object_y = event.y
#
#
# def process_text():
#     global watermark_text_object
#     text = entry_watermark.get().strip()
#     if text != "":
#         watermark_text_object = canvas.create_text(100, 100, text=text, fill=color[1])
#     else:
#         canvas.delete(watermark_text_object)
#         watermark_text_object = None
#
#
# def choose_color():
#     global color
#     color = colorDialog.show()
#
# root = tk.Tk()
#
# entry_watermark = tk.Entry()
# entry_watermark.pack()
#
# button_process_text = tk.Button(text="Add watermark", command=process_text)
# button_process_text.pack()
#
# button_choose_color = tk.Button(text="Choose color", command=choose_color)
# button_choose_color.pack()
#
#
# canvas = tk.Canvas(root, height=500, width=500)
# canvas.pack()
#
# rectangle = canvas.create_rectangle(20,20, 40, 40, fill='#474536', tags=("movable"))
# canvas.tag_bind("movable", "<Button-1>", start_moving)
# canvas.tag_bind("movable", "<ButtonRelease-1>", stop_moving)
# canvas.tag_bind("movable", "<B1-Motion>", move)
#
# colorDialog = colorchooser.Chooser(root)
#
#
# root.mainloop()