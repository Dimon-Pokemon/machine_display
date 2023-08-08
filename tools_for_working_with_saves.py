from point import Point
from json import loads
import codecs


def point_object_to_json(point: Point) -> str:
    json_string = """
{
    "x":%s,
    "y":%s,
    "id":%s,
    "state":"%s",
    "color":"%s"
}
""" % (point.x, point.y, point.id, point.state, point.color)
    return json_string


def serialization_json_string(json_string: str, encoding: str = "utf-8") -> bytes:
    byte_json_string = codecs.encode(json_string, encoding)
    result_bytes = byte_json_string + codecs.encode("0"*(1024-len(byte_json_string)), encoding)
    return result_bytes


def write_bytes(serialized_json_string, image_bytes, file_name="save.mcd"):
    with open(file_name, "wb") as file:
        file.write(serialized_json_string + image_bytes)


def get_point_from_json(json):
    dictionary = loads(json)
    return Point(dictionary["id"], dictionary["state"], dictionary["color"], dictionary["x"], dictionary["y"])


def get_point_and_image_from_save_file(save_file_name="save.mcd"):
    with open(save_file_name, "rb") as file:
        data = file.read()
    data_json: str = data[0:1024].decode("utf-8")
    data_json = data_json[0:data_json.index("}") + 1]
    point = get_point_from_json(data_json)
    data_image = data[1024::]
    return point, data_image


if __name__ == "__main__":
    point = Point(5, "Активна", "#1f1", 160, 160)
