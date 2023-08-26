from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from point import Point
from sys import platform
from tkmacosx import Button as macButton


class AddingPoint:

    def __init__(self, points_dict, combobox_points):
        self.points_dict = points_dict
        self.combobox_points = combobox_points

        window_adding_point = Toplevel()

        label_id = Label(window_adding_point, text="id точки: ")
        entry_id = Entry(window_adding_point)
        label_x = Label(window_adding_point, text="Координата x точки")
        entry_x = Entry(window_adding_point)
        label_y = Label(window_adding_point, text="Координата y точки")
        entry_y = Entry(window_adding_point)
        label_state = Label(window_adding_point, text="Состояние: ")
        combobox_state = ttk.Combobox(window_adding_point, state="readonly", values=["Активна", "Неактивна"])
        label_color = Label(window_adding_point, text="Цвет: ")
        if platform == 'darwin':
            button_color = macButton(window_adding_point, text="", width=100, command=lambda: self.set_color(button_color))
        else:
            button_color = Button(window_adding_point, text="", width=10, command=lambda: self.set_color(button_color))
        buttom_save = Button(window_adding_point, text="Добавить", command=lambda: self.add_point(entry_id, combobox_state, button_color, entry_x, entry_y, window_adding_point))
        buttom_cancel = Button(window_adding_point, text="Отмена", command=window_adding_point.quit)

        label_id.grid(row=0, column=0)
        entry_id.grid(row=0, column=1)
        label_x.grid(row=1, column=0)
        entry_x.grid(row=1, column=1)
        label_y.grid(row=2, column=0)
        entry_y.grid(row=2, column=1)
        label_state.grid(row=3, column=0)
        combobox_state.grid(row=3, column=1)
        label_color.grid(row=4, column=0)
        button_color.grid(row=4, column=1)
        buttom_save.grid(row=5, column=0)
        buttom_cancel.grid(row=5, column=1)

        window_adding_point.mainloop()

    def set_color(self, button_color):
        color_chooser = colorchooser.askcolor()
        if color_chooser[1]:
            button_color['bg'] = color_chooser[1]

    def add_point(self, entry_id, combobox_state, button_color, entry_x, entry_y, window_adding_point):
        """Метод добавляет точку на основное окно и в комбобокс с точками"""
        point = Point(
            int(entry_id.get()),
            combobox_state.get(),
            button_color["bg"],
            int(entry_x.get()),
            int(entry_y.get())
        )
        self.points_dict.update([(int(entry_id.get()), point)])
        self.combobox_points['values'] = tuple(self.points_dict.keys())
        self.combobox_points.set('')
        window_adding_point.quit()

    points_dict = None
    combobox_points = None






