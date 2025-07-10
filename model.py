import tkinter as tk
import time
from threading import Thread
from physics_objects import Vector
from base import g

class Object:
    model: tk.Canvas
    id: int
    weight: int
    coords: list[float]

    def __init__(self, model: tk.Canvas, id_: int, weight: int = 1):
        self.model = model
        self.id = id_
        self.weight = weight
        self.coords = self.model.coords(self.id)

    def delete(self):
        self.model.delete(self.id)


class MoveableObject(Object):

    speed: int
    acceleration: int
    energy: int

    def __init__(self, model: tk.Canvas, id_: int, weight: int = 1):
        super().__init__(model, id_, weight)
        self.speed = 0
        self.acceleration = 0
        self.energy = 0

    def change_coords(self, changes: tuple[float, float]):
        self.coords[0] += changes[0]
        self.coords[1] += changes[1]
        self.coords[2] += changes[0]
        self.coords[3] += changes[1]
        self.model.coords(self.id, *self.coords)

        height = self.model.height - self.coords[3]
        self.energy = (self.weight * self.speed ** 2) / 2
        print(self.speed)
    def lower_(self, points: int):
        """Сдвигает объект вниз на points точек"""
        coords = self.coords
        coords[1] += points
        coords[3] += points
        self.model.coords(self.id, *coords)


class Model(tk.Canvas):
    """Модель"""
    _objects: list
    gravity_acceleration: float
    time_: float
    tick: float

    def __init__(self, model_size: tuple[int, int], tick: int = 0.001, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = model_size[0]
        self.height = model_size[1]
        self.tick = self.time_= tick
        self._objects = []
        self.gravity_acceleration = g

        thr = Thread(target=self.__event_loop)
        thr.start()

    def __event_loop(self):
        """Цикл обработки событий"""

        while True:
            time.sleep(self.tick)
            for obj in self._objects:  # Проход по списку объектов

                if isinstance(obj, MoveableObject):  # Проверка и выбор объекта
                    for other_obj in self._objects:  # Проход по списку объектов
                        if not self.check_coords(obj.coords, other_obj.coords):   # проверка координат объекта
                            obj.change_coords(self.__get_coord_vector(obj))
                            if obj.coords[1] > self.height or obj.coords[0] > self.width or obj.coords[0] < 0 or obj.coords[3] < 0:
                                print(obj, self.width, self.height, obj.coords)
                                self._objects.remove(obj)
                                break
                self.time_ += self.tick

    def add_object(self, obj_type, obj_id: int) -> Object:
        """
        Добавляет объект в модель
        :param obj_type: тип объекта (Object или MoveableObject)
        :param obj_id: id объекта для его взаимодействия с tkinter.Canvas (возвращается методами Canvas: create_arc,
                       create_rectangle и т.п.)
        :return:
        """
        obj = obj_type(self, obj_id)
        self._objects.append(obj)
        return obj

    def __get_coord_vector(self, obj: MoveableObject) -> tuple[float, float]:
        """"""
        obj.acceleration = self.gravity_acceleration
        obj.speed = obj.acceleration * self.time_
        gravity_strength = Vector(0, 0.2)
        wind = Vector(-1, -0.1)
        res = gravity_strength + wind
        return res.x, res.y

    @staticmethod
    def check_coords(coords1: list | tuple[int, int, int, int], coords2: tuple[int, int, int, int]) -> bool:
        """
        Проверяет координаты на предмет соприкосновения
        :return: True, если нижняя часть coords1 соприкасается с верхней частью coords2. False в любом другом случае.
        """
        if (coords1[3] >= coords2[1] - 1):
            return True
        return False

    @staticmethod
    def get_center(coords: list[float]) -> tuple[float, float]:
        """
        Находит центр прямоугольника по координатам вида:
        [x1, y1, x2, y2], где (x1, y1) - координаты левого верхнего угла, (x2, y2) - координаты правого нижнего угла
        """
        return (coords[2] - ((coords[2] - coords[0]) // 2),
                coords[3] - ((coords[3] - coords[1]) // 2))

