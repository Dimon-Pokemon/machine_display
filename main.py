from app import App
from point import Point
import threading

if __name__ == "__main__":
    point1 = Point(1, "Активна", "#1f1", 160, 160)
    point2 = Point(2, "Активна", "#1f1", 150, 120)
    points_dict = {}
    # points_dict.update([(1, point1), (2, point2)])
    app = App(points_dict)
    app.build_edit_points_form()
    app.start()
    # threading.Thread(target=app.start).start()


