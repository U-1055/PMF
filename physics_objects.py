
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
