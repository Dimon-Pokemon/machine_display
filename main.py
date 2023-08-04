from app import App
from point import Point
import threading

if __name__ == "__main__":
    point = Point(5, "Активна", "#1f1", 160, 160)
    points_dict = {}
    points_dict.update([(5, point)])
    app = App(points_dict)
    app.build_input_form()
    app.start()
    # threading.Thread(target=app.start).start()


