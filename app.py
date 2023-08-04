from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from adding_point import AddingPoint


class App:
    root = Tk()
    root.geometry("1000x700")
    root.title("")
    input_form = Toplevel()
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    step_row = 25 # Расстояние между горизонтальными линиями сетки
    step_column = 25 # Расстояние между вертикальными линиями сетки

    points_dict: "List of points" = None # Словарь с точками вида "ID: point"
    select_point_id = None

    def __init__(self, points_dict, step_row=25, step_column=25):
        self.points_dict = points_dict
        self.step_row = step_row # Расстояние между горизонтальными линиями сетки
        self.step_column = step_column # Расстояние между вертикальными линиями сетки

        # Создание сетки
        for i in range(0, 1920, self.step_row):
            self.canvas.create_line(0, i, 1920, i)
        for i in range(0, 1920, self.step_column):
            self.canvas.create_line(i, 0, i, 1080)
        self.canvas.pack()

    def print_points(self):
        """
        Метод добавляет точки из словаря точек на экран, предварительно удалив все точки, чтобы
        не отображать удаленные из словаря точки.
        """
        self.canvas.delete("point") # Удаление всех точек
        # Перебор точек по их id и отрисовка их на экране
        for id_point in self.points_dict:
            if self.points_dict[id_point].state == "Активна":
                self.canvas.create_oval(self.points_dict[id_point].x - 5,
                                        self.points_dict[id_point].y - 5,
                                        self.points_dict[id_point].x + 5,
                                        self.points_dict[id_point].y + 5,
                                        fill=self.points_dict[id_point].color,
                                        tags="point") # Тэг для всех точек. По нему происходит удаление (стриание) точек

    def build_input_form(self):
        label_points = Label(self.input_form, text="Точка: ")
        combobox_points = ttk.Combobox(self.input_form, textvariable=self.select_point_id, values=list(self.points_dict.keys()), state="readonly")
        combobox_points.bind("<<ComboboxSelected>>", lambda _: self.activation_of_ui_elements(combobox_points, combobox_state, button_color, button_delete_point))
        label_state = Label(self.input_form, text="Состояние: ")
        combobox_state = ttk.Combobox(self.input_form, state="readonly", values=["Активна", "Неактивна"])
        combobox_state.bind("<<ComboboxSelected>>", lambda _: self.set_state_point(combobox_state.get()))
        label_color = Label(self.input_form, text="Цвет: ")
        button_color = Button(self.input_form, text="", bg="red", width=10, command=lambda : self.set_color(button_color))
        button_add_point = Button(self.input_form, text="Добавить новую точку", command=lambda: self.add_point(combobox_points))
        button_delete_point = Button(self.input_form, text="Удалить точку", command=self.delete_point)

        # Деактивация некоторых графических элементов (до выбора конкретной точки)
        combobox_state['state'] = 'disable'
        button_color['state'] = 'disable'
        button_delete_point['state'] = 'disable'

        # Размещение элементов интерфейса на форме
        combobox_points.grid(row=0, column=1)
        label_points.grid(row=0, column=0)
        combobox_state.grid(row=1, column=1)
        label_state.grid(row=1, column=0)
        label_color.grid(row=2, column=0)
        button_color.grid(row=2, column=1)
        button_add_point.grid(row=3, column=0)
        button_delete_point.grid(row=3, column=3)

    # Метод для активации графиечких элементов управления при выборе какой-либо точки
    def activation_of_ui_elements(self, combobox_points, combobox_state, button_color, button_delete):
        self.select_point_id = int(combobox_points.get())
        combobox_state['state'] = 'active'
        button_color['state'] = 'active'
        button_delete['state'] = 'active'

    #  Метод для добавления новой точки
    def add_point(self, combobox_points):
        AddingPoint(self.points_dict, combobox_points)

    def set_state_point(self, state):
        self.points_dict[self.select_point_id].state = state

    def delete_point(self):
        self.points_dict.pop(self.select_point_id)

    def set_color(self, colored_button):
        color_chooser = colorchooser.askcolor()
        if color_chooser[1]:
            self.points_dict[self.select_point_id].color = color_chooser[1]
            colored_button['bg'] = color_chooser[1]

    def start(self):
        while True:
            self.root.update()
            self.input_form.update()
            self.print_points()