
class Vector:

    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

    def __getitem__(self, idx):
        if idx > 1 or idx < -2:
            raise IndexError(f'This vector has only 2 components, component with index {idx} is missing')
        return [self.x, self.y][idx]

    def __mul__(self, other):
        if isinstance(other, Vector):  # скалярное произведение векторов
            return self.x * other.x + self.y * other.y
        elif isinstance(other, int | float):  # вектор с произведением исходных компонент на введённый скаляр
            return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        if isinstance(other, Vector):
            pass
        elif isinstance(other, int | float):
            return Vector(self.x * other, self.y * other)

    def __neg__(self):
        return Vector(-self.x, -self.y)



class Force(Vector):
    """
    Сила. Является подклассом вектора, содержит дополнительный параметры obj и time_.

    :param x: координаты вектора по Ox.
    :param y: координаты вектора по Oy.
    :param obj: объект, на который действует сила.
    :param time_: время (мс) действия силы на объект. Если меньше 2 - действует бесконечно.
    """

    def __init__(self, x: float, y: float, obj, time_: int = 2): # Т.к. 2 мс - минимальное время для обработки силы движком
        super().__init__(x, y)
        self.__obj = obj
        self.__time = int(time_)

        if time_ >= 1:
            obj.model.after(self.__time, lambda: obj.stop_force(self))

    def __neg__(self):
        return Force(-self.x, -self.y, self.__obj, self.__time)


class SetList(set):

    def __init__(self, *args):
        super().__init__(*args)

    def __getitem__(self, idx: int):
        if idx < 0 or idx >= len(self):
            raise IndexError

        for i, value in enumerate(self):
            if i == idx:
                return value
