class Agent:
    """
    Agent class built by data from the server.
    """

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: str) -> None:
        self._id = id
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        x, y, _ = pos.split(",")
        self._pos = (float(x), float(y), 0.0)

    def get_pos(self) -> tuple:
        return self._pos

    def get_id(self) -> int:
        return self._id

    def get_src(self) -> int:
        return self._src

    def get_dest(self) -> int:
        return self._dest

    def get_speed(self) -> float:
        return self._speed

    def get_value(self) -> float:
        return self._value
