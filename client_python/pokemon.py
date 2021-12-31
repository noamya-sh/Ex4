class pokemon:
    def __init__(self, v, t, pos) -> None:
        self._value = v
        self._type = t
        x, y, z = pos.split(",")
        self._pos = (float(x), float(y), float(z))
