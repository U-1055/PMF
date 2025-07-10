import tkinter as tk
import time
from threading import Thread


class Object:  # ToDo: продумать необходимость Object и MoveableObject
    model: tk.Canvas
    id: int
    weight: int
    coords: list[float]

    def __init__(self, model: tk.Canvas, id_: int, weight: int = 0):
        self.model = model
        self.id = id_
        self.weight = weight
        self.coords = self.model.coords(self.id)

    def delete(self):
        self.model.delete(self.id)


class MoveableObject(Object):

    speed: int
    acceleration: int

    def __init__(self, model: tk.Canvas, id_: int, weight: int = 0):
        super().__init__(model, id_, weight)
        self.speed = 0
        self.acceleration = 0

    def change_coords(self, coords: tuple[int, int, int, int]):
        self.model.coords(self.id, coords)

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

    def __init__(self, model_size: tuple[int, int], tick: int = 0.001, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = model_size[0]
        self.height = model_size[1]
        self.tick = tick
        self._objects = []

        thr = Thread(target=self.__event_loop)
        thr.start()

    def __event_loop(self):
        """Цикл обработки событий"""

        while True:
            time.sleep(self.tick)
            for obj in self._objects:  # Проход по списку объектов

                if isinstance(obj, MoveableObject):  # Проверка и выбор объекта
                    for other_obj in self._objects:  # Проход по списку объектов
                        if not self.check_coords(obj.coords, other_obj.coords) and not isinstance(other_obj, MoveableObject):   # проверка координат объекта
                            obj.lower_(1)
                            if obj.coords[1] > self.height or obj.coords[0] > self.width:
                                print(obj, self.width, self.height, obj.coords)
                                self._objects.remove(obj)
                                break

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

    @staticmethod
    def check_coords(coords1: list | tuple[int, int, int, int], coords2: tuple[int, int, int, int]) -> bool:
        """
        Проверяет координаты на предмет соприкосновения
        :return: True, если нижняя часть coords1 соприкасается с верхней частью coords2. False в любом другом случае.
        """
        if (coords1[3] == coords2[1] - 1):
            return True
        return False

