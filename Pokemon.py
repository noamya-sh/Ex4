class Pokemon:
    """
    Pokemon class built by data from the server.
    """

    def __init__(self, value: float, type: int, pos: str) -> None:
        self._value = value
        self._type = type
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)

    def get_pos(self) -> tuple:
        return self._pos

    def get_type(self) -> int:
        return self._type

    def get_value(self) -> float:
        return self._value

    def __eq__(self, other):
        return self._pos == other._pos
