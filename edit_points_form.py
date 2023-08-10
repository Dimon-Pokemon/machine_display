from tkinter import *
from tkinter import ttk
from tkinter import colorchooser


def validate_coordinate_entry(data: str) -> bool:
    if data.isdigit() or data == '':
        return True
    return False


class EditPointsForm:
    main_app_ref = None
    # root = None
    # select_point_id = None
    # points_dict = None

    input_form = None

    button_previous_point = None
    button_next_point = None
    label_points = None
    combobox_points = None
    label_state = None
    combobox_state = None
    label_color = None
    button_color = None
    label_x = None
    entry_x = None
    label_y = None
    entry_y = None
    button_add_point = None
    button_delete_point = None

    def __init__(self, main_app_ref, root=None):
        self.main_app_ref = main_app_ref
        # self.root = root
        self.input_form = Toplevel()
        self.input_form.focus_set()
        self.label_points = Label(self.input_form, text="Точка: ")
        self.combobox_points = ttk.Combobox(self.input_form,
                                            values=list(self.main_app_ref.points_dict.keys()), state="readonly")
        self.combobox_points.bind("<<ComboboxSelected>>",
                                  lambda _: self.main_app_ref.activation_of_ui_elements(self.combobox_points,
                                                                                        self.combobox_state,
                                                                                        self.button_color,
                                                                                        self.button_delete_point,
                                                                                        self.label_x,
                                                                                        self.label_y,
                                                                                        self.entry_x,
                                                                                        self.entry_y, ))
        self.input_form.bind("<Right>",
                             lambda _: self.main_app_ref.select_next_or_previous_point(self.combobox_points,
                                                                                       self.combobox_state,
                                                                                       self.button_color,
                                                                                       self.button_delete_point,
                                                                                       self.label_x, self.label_y,
                                                                                       self.entry_x, self.entry_y,
                                                                                       "next"))
        self.input_form.bind("<Left>",
                             lambda _: self.main_app_ref.select_next_or_previous_point(self.combobox_points,
                                                                                       self.combobox_state,
                                                                                       self.button_color,
                                                                                       self.button_delete_point,
                                                                                       self.label_x, self.label_y,
                                                                                       self.entry_x, self.entry_y,
                                                                                       "previous"))
        self.label_state = Label(self.input_form, text="Состояние: ")
        self.combobox_state = ttk.Combobox(self.input_form, state="readonly", values=["Активна", "Неактивна"])
        self.combobox_state.bind("<<ComboboxSelected>>",
                                 lambda _: self.main_app_ref.set_state_point(self.combobox_state.get()))
        self.label_color = Label(self.input_form, text="Цвет: ")
        self.button_color = Button(self.input_form, text="", bg="red", width=10,
                                   command=lambda: self.main_app_ref.set_color(self.button_color))
        self.button_add_point = Button(self.input_form, text="Добавить новую точку",
                                       command=lambda: self.main_app_ref.add_point(self.combobox_points,
                                                                                   self.combobox_state))
        self.button_delete_point = Button(self.input_form, text="Удалить точку",
                                          command=lambda: self.main_app_ref.delete_point(self.combobox_points))

        self.button_next_point = Button(self.input_form, text=">>",
                                        command=lambda: self.main_app_ref.select_next_or_previous_point(
                                            self.combobox_points,
                                            self.combobox_state,
                                            self.button_color,
                                            self.button_delete_point,
                                            self.label_x,
                                            self.label_y,
                                            self.entry_x,
                                            self.entry_y,
                                            "next"))
        self.button_previous_point = Button(self.input_form, text="<<",
                                            command=lambda: self.main_app_ref.select_next_or_previous_point(
                                                self.combobox_points,
                                                self.combobox_state,
                                                self.button_color,
                                                self.button_delete_point,
                                                self.label_x,
                                                self.label_y, self.entry_x,
                                                self.entry_y,
                                                "previous"))
        self.validate_command = (self.input_form.register(validate_coordinate_entry), '%P')
        self.label_x = Label(self.input_form, text="Координата x точки:")
        self.entry_x = Entry(self.input_form, validate="key", validatecommand=self.validate_command)
        self.entry_x.bind('<KeyRelease>', lambda _: self.main_app_ref.change_point_coordinate(entry_x=self.entry_x))
        self.label_y = Label(self.input_form, text="Координата y точки:")
        self.entry_y = Entry(self.input_form, validate="key", validatecommand=self.validate_command)
        self.entry_y.bind('<KeyRelease>', lambda _: self.main_app_ref.change_point_coordinate(entry_y=self.entry_y))

        # Деактивация некоторых графических элементов (до выбора конкретной точки)
        self.combobox_state['state'] = 'disable'
        self.button_color['state'] = 'disable'
        self.button_delete_point['state'] = 'disable'
        self.label_x['state'] = 'disable'
        self.entry_x['state'] = 'disable'
        self.label_y['state'] = 'disable'
        self.entry_y['state'] = 'disable'

        # Размещение элементов интерфейса на форме
        self.button_previous_point.grid(row=0, column=0, sticky="nw")
        self.button_next_point.grid(row=0, column=2, sticky="ne")
        self.combobox_points.grid(row=1, column=1)
        self.label_points.grid(row=1, column=0)
        self.combobox_state.grid(row=2, column=1)
        self.label_state.grid(row=2, column=0)
        self.label_color.grid(row=3, column=0)
        self.button_color.grid(row=3, column=1)
        self.label_x.grid(row=4, column=0)
        self.entry_x.grid(row=4, column=1)
        self.label_y.grid(row=5, column=0)
        self.entry_y.grid(row=5, column=1)
        self.button_add_point.grid(row=6, column=0)
        self.button_delete_point.grid(row=6, column=2)

        if self.main_app_ref.select_point_id:
            self.combobox_points.set(str(self.main_app_ref.select_point_id))
            self.main_app_ref.activation_of_ui_elements(self.combobox_points,
                                                        self.combobox_state,
                                                        self.button_color,
                                                        self.button_delete_point,
                                                        self.label_x, self.label_y,
                                                        self.entry_x, self.entry_y)

    def select_new_point_and_display_on_edit_point_form(self, point_id):
        self.combobox_points.set(str(point_id))
        self.main_app_ref.activation_of_ui_elements(self.combobox_points,
                                                    self.combobox_state,
                                                    self.button_color,
                                                    self.button_delete_point,
                                                    self.label_x, self.label_y,
                                                    self.entry_x, self.entry_y)
