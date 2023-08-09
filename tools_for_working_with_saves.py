from point import Point
from json import loads
import codecs


def point_objects_to_json(points: dict[Point]) -> str:
    json_string = """{"""
    for id_point in points.keys():
        point_json_string = """
    "%s":{
        "x":%s,
        "y":%s,
        "id":%s,
        "state":"%s",
        "color":"%s"
    },""" % (
            points[id_point].id, points[id_point].x, points[id_point].y, points[id_point].id, points[id_point].state,
            points[id_point].color)
        json_string += point_json_string
    json_string = json_string[:len(json_string) - 1] + "\n}"
    return json_string


def serialization_json_string(json_string: str, encoding: str = "utf-8") -> bytes:
    byte_json_string = codecs.encode(json_string, encoding)
    result_bytes = byte_json_string + codecs.encode("0" * (1024 - len(byte_json_string)), encoding)
    return result_bytes


def write_bytes(serialized_json_string, image_bytes, file_name="save.mcd"):
    """
    Метод для записи файла сохранения.
    Файл сохранения включает в себя изображение и информацию о
    размещенных на нем точках в формате Json
    """
    if file_name.count(".mcd") == 1:
        with open(file_name, "wb") as file:
            file.write(serialized_json_string + image_bytes)
    else: # Пользователь не указал расширение файла сохранения
        with open(file_name+".mcd", "wb") as file: # Добавляем нужное расширение вручную
            file.write(serialized_json_string + image_bytes)


def get_points_dict_from_json(json):
    print(json)
    dict_points_info_from_json = loads(json)
    points_dict = {}
    for id_point in dict_points_info_from_json.keys():
        dict_for_point = dict_points_info_from_json[id_point]
        point = Point(dict_for_point["id"], dict_for_point["state"], dict_for_point["color"], dict_for_point["x"], dict_for_point["y"])
        points_dict.update([(int(id_point), point)])
    return points_dict


def get_point_and_image_from_save_file(bytes_file_save, save_file_name=None):
    if save_file_name is None:
        data = bytes_file_save
    else:
        with open(save_file_name, "rb") as file:
            data = file.read()
    data_json: str = data[0:1024].decode("utf-8")
    data_json = data_json[::-1]
    close_brace_index = data_json.find("}")
    if close_brace_index > 0:
        data_json = data_json[close_brace_index::]
        data_json = data_json[::-1]
    print(data_json)
    point = get_points_dict_from_json(data_json)
    data_image = data[1024::]
    return point, data_image


if __name__ == "__main__":
    point = Point(5, "Активна", "#1f1", 160, 160)
    get_point_and_image_from_save_file()
