from tkinter import *
from tkinter import ttk
from tkinter import colorchooser


class App:
    root = Tk()
    root.geometry("1000x700")
    input_form = Tk()
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    step_row = 25
    step_column = 25
    points: "List of points" = {}

    select_point = None

    def __init__(self, step_row=25, step_column=25):
        self.step_row = step_row
        self.step_column = step_column

        for i in range(0, 1920, self.step_row):
            self.canvas.create_line(0, i, 1920, i)
        for i in range(0, 1920, self.step_column):
            self.canvas.create_line(i, 0, i, 1080)
        self.canvas.pack()

    def print_points(self):
        self.canvas.delete("point") # Удаление всех точек
        # Перебор точек по их id и отрисовка их на экране
        for id_point in self.points:
            self.canvas.create_oval(self.points[id_point].x-5,
                                    self.points[id_point].y-5,
                                    self.points[id_point].x+5,
                                    self.points[id_point].y+5,
                                    fill=self.points[id_point].color,
                                    tags="pointl") # Тэг для всех точек. По нему происходит удаление (стриание) точек

    def build_input_form(self):
        # lbl_space = Label(self.input_form, text="         ")
        lbl_points = Label(self.input_form, text="Точка: ")
        cb_points = ttk.Combobox(self.input_form, textvariable=self.select_point, values=list(self.points.keys()), state="readonly")
        cb_points.bind("<<ComboboxSelected>>", lambda _: self.activation_of_ui_elements(cb_points, cb_state, btn_color))
        lbl_state = Label(self.input_form, text="Состояние: ")
        cb_state = ttk.Combobox(self.input_form, state="readonly")
        lbl_color = Label(self.input_form, text="Цвет: ")
        btn_color = Button(self.input_form, text="", bg="red", width=10, command=lambda : self.set_color(btn_color))
        btn_add_point = Button(self.input_form, text="Добавить новую точку", command=self.add_point)
        btn_delete_point = Button(self.input_form, text="Удалить точку", command=self.delete_point)

        cb_state['state'] = 'disable'
        btn_color['state'] = 'disable'

        cb_points.grid(row=0, column=1)
        lbl_points.grid(row=0, column=0)
        cb_state.grid(row=1, column=1)
        lbl_state.grid(row=1, column=0)
        lbl_color.grid(row=2, column=0)
        btn_color.grid(row=2, column=1)
        btn_add_point.grid(row=3, column=0)
        btn_delete_point.grid(row=3, column=3)

    def activation_of_ui_elements(self, combobox_points, combobox_state, button_color):
        self.select_point = int(combobox_points.get())
        combobox_state['state'] = 'active'
        button_color['state'] = 'active'

    def add_point(self):
        pass

    def delete_point(self):
        self.points.pop(self.select_point)

        # self.points

    def set_color(self, colored_button):
        color_chooser = colorchooser.askcolor()
        if color_chooser[1]:
            self.points[self.select_point].color = color_chooser[1]
            colored_button['bg'] = color_chooser[1]
            # self.input_form.children['!button']['bg'] = color_chooser[1]



    def start(self):
        while True:
            self.root.update()
            self.input_form.update()
            self.print_points()