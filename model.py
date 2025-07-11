import tkinter as tk
import time
from threading import Thread

import pylab as pl

from physics_objects import Vector
from base import g


class Object:
    model: tk.Canvas
    id: int
    weight: float
    coords: list[float]
    forces: list[Vector]

    def __init__(self, model: tk.Canvas, id_: int, weight: float = 1):
        self.model = model
        self.id = id_
        self.weight = weight
        self.coords = self.model.coords(self.id)
        self.forces = [Vector(0, self.model.gravity_acceleration * weight), -Vector(0, self.model.resistance * weight)]  # ToDo: продумать вопрос с F сопротивления

    def delete(self):
        self.model.delete(self.id)


class MoveableObject(Object):
    """
    Подвижный объект
    :param speed: скорость объекта (м/с)
    :param acceleration: ускорение объекта (м/с^2)
    :param energy: энергия объекта (Дж) ToDo: какая энергия?
    """
    speed: Vector
    acceleration: Vector
    energy: int

    def __init__(self, model: tk.Canvas, id_: int, weight: float = 1):
        super().__init__(model, id_, weight)
        self.speed = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.energy = 0

        self.speeds = [0]
        self.accelerations = [0]
        self.times = [0.]

    def change_coords(self, force: Vector, tick: float, time_: float):
        print(self.forces, force.x, force.y)
        self.acceleration = Vector(force.x / self.weight, force.y / self.weight)  # F=ma -> a = F/m
        print(self.acceleration.y, self.speed.y)
        self.speed = self.acceleration * 0.001 + self.speed  # V = V0 + a*dt
        print(self.speed.y)

        #new_speed = self.speed + force
        self.coords[0] += self.speed[0]
        self.coords[1] += self.speed[1]
        self.coords[2] += self.speed[0]
        self.coords[3] += self.speed[1]
        self.model.coords(self.id, *self.coords)

        self.speeds.append(self.speed.y)
        self.accelerations.append(self.acceleration.y)
        self.times.append(time_)

    def lower_(self, points: int):
        """Сдвигает объект вниз на points точек"""
        coords = self.coords
        coords[1] += points
        coords[3] += points
        self.model.coords(self.id, *coords)

    def plot_data(self):
        pl.plot(self.times, self.speeds)
        pl.show()
        pl.plot(self.times, self.accelerations)
        pl.show()


class Model(tk.Canvas):
    """Модель"""
    _objects: list
    gravity_acceleration: float
    time_: float
    tick: float
    resistance: float

    def __init__(self, model_size: tuple[int, int], tick: float = 0.001, gravity_acceleration: float = g, resistance: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = model_size[0]
        self.height = model_size[1]
        self.tick = self.time_ = tick
        self.resistance = resistance
        self._objects = []
        self.gravity_acceleration = g

        self.processing = True
        thr = Thread(target=self.__event_loop)
        thr.start()
        self.processing = False

    def __event_loop(self):
        """Цикл обработки событий"""

        while True:
            if not self.processing:
                continue

            time.sleep(self.tick)
            for obj in self._objects:  # Проход по списку объектов

                if isinstance(obj, MoveableObject):  # Проверка и выбор объекта
                    for other_obj in self._objects:  # Проход по списку объектов
                        if not self.check_coords(obj.coords, other_obj.coords):   # проверка координат объекта
                            obj.change_coords(self.__get_coord_vector(obj), self.tick, self.time_)
                            self.create_oval(*self.get_center(obj.coords), *[x + 1 for x in self.get_center(obj.coords)])
                            if obj.coords[1] > self.height or obj.coords[0] > self.width or obj.coords[0] < 0 or obj.coords[3] < 0:
                                print(obj, self.width, self.height, obj.coords)
                                self._objects.remove(obj)
                                obj.delete()
                                break
                self.time_ += self.tick

    def add_object(self, obj_type, obj_id: int, weight: float = 1) -> Object:
        """
        Добавляет объект в модель
        :param obj_type: тип объекта (Object или MoveableObject)
        :param obj_id: id объекта для его взаимодействия с tkinter.Canvas (возвращается методами Canvas: create_arc,
                       create_rectangle и т.п.)
        :param weight: вес объекта (кг).
        :return:
        """
        obj = obj_type(self, obj_id, weight)
        self._objects.append(obj)
        return obj

    def __get_coord_vector(self, obj: MoveableObject) -> Vector:
        """"""
        result_force = Vector(0, 0)
        for force in obj.forces:
            result_force += force

        return result_force

    def start_processing(self):
        self.processing = True

    def stop_processing(self):
        self.processing = False

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

