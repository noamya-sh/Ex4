class Pokemon:

    def __init__(self, value, type, pos) -> None:
        self._value = value
        self._type = type
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)

    def get_pos(self):
        return self._pos

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value

    def __eq__(self, other):
        return self._pos == other._pos
