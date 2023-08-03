from app import App
from point import Point
import threading

if __name__ == "__main__":
    app = App()
    point = Point(5, 0, "#1f1", 160, 160, 20)
    app.points.update([(5, point)])
    app.build_input_form()
    app.start()
    # threading.Thread(target=app.start).start()


