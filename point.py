class Point:

    x = 0
    y = 0
    r = 0
    id = None
    state = None
    color = None

    def __init__(self, id, state, color, x=0, y=0, r=6):
        self.x = x
        self.y = y
        self.id = id
        self.state = state
        self.color = color
