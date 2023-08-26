from tkinter import *
from sys import platform
from tkinter import colorchooser
from tkinter import filedialog
from adding_point import AddingPoint
from tools_for_working_with_saves import *
from edit_points_form import EditPointsForm


# def validate_coordinate_entry(data: str) -> bool:
#     if data.isdigit() or data == '':
#         return True
#     return False


class App:
    image_formats = ("pgm", "ppm", "gif", "png")

    root = Tk()
    root.geometry("1000x700")
    root.title("Дисплейные точки")
    canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    input_form_window = None # Окно редактирования точек
    input_form_class = None

    path_to_image = None  # не знаю, нужно ли это
    bytes_image = None
    image = None

    points_dict: "List of points" = {}  # Словарь с точками вида "id: Point"
    select_point_id = None

    def __init__(self, points_dict):
        if points_dict:
            self.points_dict = points_dict
        else:
            self.points_dict = {}
        self.canvas.bind('<Button-1>', lambda _: self.select_point_on_click_mouse_button())
        self.canvas.pack()

        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        filemenu.add_command(label="Открыть...", command=self.open_new_image_or_file_save)
        filemenu.add_command(label="Сохранить", command=self.save)
        filemenu.add_command(label="Отобразить редактор точек", command=self.build_edit_points_form)
        filemenu.add_command(label="Начать сварку", command=self.start)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.root.destroy)
        menu.add_cascade(label="Файл", menu=filemenu)

    def set_image(self, bytes_image):
        image = PhotoImage(data=bytes_image)
        self.root.geometry(f"{image.width()}x{image.height()}")
        self.image = image
        self.canvas.create_image(0, 0, image=image, anchor="nw")

    def select_point_on_click_mouse_button(self):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        for point in self.points_dict.values():
            if point.x-5 < x < point.x+5 and point.y-5< y < point.y+5:
                if self.select_point_id:
                    print("Замена выбранно точки ", self.select_point_id, " на новую точку ", point.id)
                    # self.select_point_id = point.id
                    self.input_form_class.select_new_point_and_display_on_edit_point_form(point.id)
                else:
                    self.select_point_id = point.id
                    if self.input_form_window:
                        self.input_form_class.select_new_point_and_display_on_edit_point_form(self.select_point_id)
                    print("Выбрана точка: ", self.select_point_id)

    def start(self):
        pass

    def open_save(self, bytes_file_save=None):
        """
        Метод открывает сохранение.
        :arg bytes_file_save - считанные из файла сохранения байты
        Если параметр bytes_file_save не задан, то открывается диалоговое окно для выбора файла сохранения и
        в метод get_point_and_image_from_save_file передается путь до файла в параметр save_file_name
        Если параметр bytes_file_save ЗАДАН,  то в метод get_point_and_image_from_save_file передается данный параметр
        в качестве аргумента bytes_file_save
        """
        if bytes_file_save is None:  # Если не были переданы байты, считанные с файла сохранения
            path_to_save_file = filedialog.askopenfilename()  # Спрашиваем путь до файла сохранения
            points_dict, bytes_image = get_point_and_image_from_save_file(save_file_name=path_to_save_file)
        else:
            points_dict, bytes_image = get_point_and_image_from_save_file(bytes_file_save=bytes_file_save)

        self.points_dict = points_dict
        self.set_image(bytes_image)

    def open_new_image_or_file_save(self):
        """Метод для открытия нового изображения для редактирования или файла сохранения"""
        file_path = filedialog.askopenfilename()
        self.path_to_image = file_path
        with open(file=file_path, mode="rb") as file:
            bytes_image_or_file_save = file.read()
            self.bytes_image = bytes_image_or_file_save
        if file_path[len(file_path) - 3:] in self.image_formats:
            self.set_image(bytes_image_or_file_save)
        else:
            self.open_save(bytes_file_save=bytes_image_or_file_save)

    def save(self):
        """Метод для сохранения изображения с размещенными на нем точками"""
        file_name = filedialog.asksaveasfilename()
        json_point_info = point_objects_to_json(self.points_dict)
        serialization_json_point_info = serialization_json_string(json_point_info)
        write_bytes(serialization_json_point_info, self.bytes_image, file_name)

    def print_points(self):
        """
        Метод добавляет точки из словаря точек на экран, предварительно удалив все точки, чтобы
        не отображать удаленные из словаря точки.
        """
        self.canvas.delete("point")  # Удаление всех точек
        # Перебор точек по их id и отрисовка их на экране
        for id_point in self.points_dict:
            if self.points_dict[id_point].state == "Активна":
                self.canvas.create_oval(self.points_dict[id_point].x - 5,
                                        self.points_dict[id_point].y - 5,
                                        self.points_dict[id_point].x + 5,
                                        self.points_dict[id_point].y + 5,
                                        fill=self.points_dict[id_point].color,
                                        tags="point")  # Тэг для всех точек. По нему происходит удаление (стриание) точек

    def build_edit_points_form(self):
        self.input_form_class = EditPointsForm(self)
        self.input_form_window = self.input_form_class.input_form

    def change_point_coordinate(self, entry_x: Entry = None, entry_y: Entry = None):
        if entry_x:
            entry_x_data = entry_x.get()
            if entry_x_data != '':
                self.points_dict[self.select_point_id].x = int(entry_x_data)
        elif entry_y:
            entry_y_data = entry_y.get()
            if entry_y_data != '':
                self.points_dict[self.select_point_id].y = int(entry_y_data)
        else:
            print("Error")

    # Метод для активации графиечких элементов управления при выборе какой-либо точки
    def activation_of_ui_elements(self, combobox_points, combobox_state, button_color: Button, button_delete, label_x, label_y, entry_x: Entry, entry_y):
        self.select_point_id = int(combobox_points.get())
        combobox_state['state'] = 'active'
        combobox_state.set(self.points_dict[self.select_point_id].state)
        button_color['state'] = 'active'
        if platform == 'darwin':
            button_color['activebackground'] = self.points_dict[self.select_point_id].color
        else:
            button_color['background'] = self.points_dict[self.select_point_id].color
        button_delete['state'] = 'active'
        label_x['state'] = 'active'
        entry_x['state'] = 'normal'
        entry_x.delete(0, 'end')
        entry_x.insert(END, str(self.points_dict[self.select_point_id].x))
        label_y['state'] = 'active'
        entry_y['state'] = 'normal'
        entry_y.delete(0, 'end')
        entry_y.insert(END, str(self.points_dict[self.select_point_id].y))

    def select_next_or_previous_point(self, combobox_points, combobox_state, button_color, button_delete_point, label_x, label_y, entry_x, entry_y, pointer):
        """
        Метод выбирает следующую или предыдущую точку при нажатии стрелочки <- ->, а затем
        вызывает метод для активации графических элементов для редактирования
        """
        # Проверка на наличие точек. Если точек нет, то метод завершает свое выполнение
        if len(self.points_dict) == 0:
            return  # досрочное завершение работы метода

        points = list(self.points_dict.keys())  # Массив ключей
        points.sort()

        if self.select_point_id:
            index = points.index(self.select_point_id)  # Получаем индекс ключа в списке ключей
            # Если выбрана последняя точка и нажата клавиша ->(выбрать СЛЕДУЮЩУЮ точку), то
            if index == len(self.points_dict) - 1 and pointer == "next":
                self.select_point_id = points[0]  # Берем ПЕРВУЮ точку
            # Если выбрана первая точка и нажата клавиша <-(выбрать ПРЕДЫДУЩУЮ точку), то
            elif index == 0 and pointer == "previous":
                self.select_point_id = points[len(self.points_dict) - 1]  # Берем ПОСЛЕДНЮЮ точку
            else:
                if pointer == "next":
                    self.select_point_id = points[index + 1]
                else:
                    self.select_point_id = points[index - 1]
            combobox_points.set(self.select_point_id)
        else:
            if len(self.points_dict) > 0:  # Если есть точки
                self.select_point_id = points[0]  # Сохраняем id выбранной точки
                combobox_points.set(points[0])  # Выбираем первую точку в ComboBox
        self.activation_of_ui_elements(combobox_points, combobox_state, button_color, button_delete_point, label_x, label_y, entry_x, entry_y,)

    #  Метод для добавления новой точки
    def add_point(self, combobox_points, combobox_state):
        AddingPoint(self.points_dict, combobox_points)
        combobox_state.set('')

    def set_state_point(self, state):
        self.points_dict[self.select_point_id].state = state

    def delete_point(self, combobox_points):
        self.points_dict.pop(self.select_point_id)
        self.select_point_id = None
        combobox_points['values'] = tuple(self.points_dict.keys())
        combobox_points.set('')

    def set_color(self, colored_button):
        color_chooser = colorchooser.askcolor()
        if color_chooser[1]:
            self.points_dict[self.select_point_id].color = color_chooser[1]
            colored_button['bg'] = color_chooser[1]

    def start(self):
        while True:
            self.root.update()
            if self.input_form_window:
                self.input_form_window.update()
            self.print_points()
