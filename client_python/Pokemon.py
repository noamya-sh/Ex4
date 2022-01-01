class Pokemon:

    def __init__(self, value, type, pos) -> None:
        self._value = value
        self._type = type
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)
