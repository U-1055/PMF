import tkinter as tk
import time
from threading import Thread
from typing import Callable

import pylab as pl

from physics_objects import Vector, Force, SetList
from base import g


class Object:
    id: int
    weight: float
    coords: list[float]
    forces: set[Vector]
    strength: int  # прочность

    def __init__(self, model: tk.Canvas, id_: int, weight: float = 1):
        self.model = model
        self.id = id_
        self.weight = weight
        self.coords = self.model.coords(self.id)
        self.forces = set((Vector(0, self.model.gravity_acceleration) * self.weight, self.model.resistance * weight))  # ToDo: продумать вопрос с F сопротивления
        self.strength = 100

    def delete(self):
        self.model.delete(self.id)
        del self

    def check_strength(self):
        if self.strength == 0:
            self.delete()

    def stop_force(self, force: Force):
        """Прекращает действие силы на объект (удаляет эту силу из списка)"""
        print(self.id)
        try:
            self.forces.remove(force)
        except KeyError:
            pass
        del force

    def get_res_force(self) -> Vector:
        """Возвращает векторную сумму сил, действующих на объект"""
        result_force = Vector(0, 0)
        for force in self.forces:
            result_force += force

        return result_force


class MoveableObject(Object):
    """
    Подвижный объект
    :param speed: скорость объекта (м/с)
    :param acceleration: ускорение объекта (м/с^2)
    """
    speed: Vector
    acceleration: Vector
    tracing: bool
    __impact_callback: Callable

    def __init__(self, model: tk.Canvas, id_: int, weight: float = 1, tracing: bool = True, impact_callback: Callable = lambda: None):
        super().__init__(model, id_, weight=weight)
        self.speed = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.tracing = tracing
        self.__impact_callback = impact_callback

        self.speeds = [0.]
        self.accelerations = [0.]
        self.times = [0.]
        self.res_forces_y = [0.]
        self.res_forces_x = [0.]

        self.forced = False

    def change_coords(self, time_: float):

        force = self.get_res_force()

        self.acceleration = Vector(force.x / self.weight, force.y / self.weight)  # F=ma -> a = F/m
        self.speed = self.acceleration * self.model.tick + self.speed  # V = V0 + a*dt

        self.coords[0] += self.speed[0]
        self.coords[1] += self.speed[1]
        self.coords[2] += self.speed[0]
        self.coords[3] += self.speed[1]
        self.model.coords(self.id, *self.coords)

        self.speeds.append(self.speed.y)
        self.accelerations.append(self.acceleration.y)
        self.times.append(time_)
        self.res_forces_y.append(force.y)
        self.res_forces_x.append(force.x)

        if self.tracing:
            center_coords = self.model.get_center(self.coords)
            self.model.create_oval(*center_coords, *(coord + 1 for coord in center_coords))

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
        pl.plot(self.times, self.res_forces_x)
        pl.show()
        pl.plot(self.times, self.res_forces_y)
        pl.show()

    def prepare_impact(self, obj2: 'Object', time_: float):
        """Стандартная функция обработки столкновений"""
        force = self.acceleration * self.weight

        if force.x == 0 and force.y == 0:
            return
        if len(self.forces) > 2:
            return

        obj2.forces.add(Force(force.x, force.y, obj2, self.model.tick * 1000 * 2))  # * 1000,  т.к. tick - с, а Force принимает в мс (1 с = 1000 мс)
        obj2_res_force = -obj2.get_res_force()

        self.forces.add(Force(obj2_res_force.x, obj2_res_force.y, self, self.model.tick * 1000 * 2))

        self.change_coords(time_)


class Model(tk.Canvas):
    """Модель"""
    __objects: list[Object]
    __gravity_acceleration: float
    __time_: float
    __tick: float
    __resistance: Vector

    def __init__(
            self,
            model_size: tuple[int, int],
            tick: float = 0.001,
            gravity_acceleration: float = g,
            resistance: Vector = Vector(0, 0),
            *args, **kwargs
    ):

        super().__init__(*args, **kwargs)
        self.__width = model_size[0]
        self.__height = model_size[1]
        self.__tick = self.time_ = tick
        self.__resistance = resistance
        self.__objects = []
        self.__gravity_acceleration = gravity_acceleration

        self.__root = ''
        self.__model = tk.Canvas()

        self.processing = True
        thr = Thread(target=self.__event_loop)
        thr.start()
        self.processing = False

    def __event_loop(self):
        """Цикл обработки событий"""

        while True:
            if not self.processing:
                continue

            time.sleep(self.__tick)
            for obj in self.__objects:  # Проход по списку объектов

                if isinstance(obj, MoveableObject):  # Проверка на подвижность объекта
                    for other_obj in self.__objects:  # Проход по списку объектов

                        if other_obj == obj:
                            continue

                        if self.check_coords(obj.coords, other_obj.coords):   # проверка на столкновение
                            obj.prepare_impact(other_obj, self.time_)
                        else:
                            obj.change_coords(self.time_)

                        if obj.coords[1] > self.__height or obj.coords[0] > self.__width or obj.coords[0] < 0 or obj.coords[3] < 0:
                           # self.delete_object(obj)
                            break
                self.time_ += self.__tick

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
        self.__objects.append(obj)
        return obj

    def start_processing(self):
        self.processing = True

    def stop_processing(self):
        self.processing = False

    def delete_object(self, obj: Object):
        """Удаляет объект."""
        self.__objects.remove(obj)
        obj.delete()

    def create_window_(self, width: int = None, height: int = None, padding: str = tk.CENTER):
        """
        Создаёт основное окно.

        :param width: ширина окна (в пикселях)
        :param height: высота окна (в пикселях)
        :param padding: выравнивание окна на экране. Значение по умолчанию: tk.CENTER
                        Принимает значения:
                        tk.CENTER - выравнивание по центру
                        tk.TOP - выравнивание по верхней границе
                        tk.BOTTOM - выравнивание по нижней границе
                        tk.LEFT - выравнивание по левому краю
                        tk.RIGHT - выравнивание по правому краю
        """

        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        if (width is None) or (width > screen_width) or (width <= 0):  # Проверка на соответствие (ширина и высота должны быть больше 0 и меньше ширины/высоты экрана)
            width = screen_width
        if (height is None) or (height > screen_height) or (height <= 0):
            height = screen_height

        padx, pady = 0, 0  # Проверка отступа
        if padding == tk.CENTER:
            padx = (screen_width - width) / 2
            pady = (screen_height - height) / 2
        elif padding == tk.BOTTOM:
            pady = screen_height - height
        elif padding == tk.TOP or padding == tk.LEFT:  # Ничего не происходит, т.к. padx и pady равны нулю
            pass
        elif padding == tk.RIGHT:
            padx = screen_width - width

        self.__root.geometry(f'{width}x{height}+{padx}+{pady}')
        self.__root.mainloop()

    @property
    def objects(self) -> list[Object]:
        return self.__objects

    @property
    def time(self) -> float:
        return self.__time_

    @property
    def resistance(self) -> Vector:
        return self.__resistance

    @property
    def gravity_acceleration(self) -> float:
        return self.__gravity_acceleration

    @property
    def tick(self) -> float:
        return self.__tick

    @staticmethod
    def check_coords(coords1: list[int | float] | tuple[int | float, ...], coords2: list[int | float] | tuple[int | float, ...]) -> bool:
        """
        Проверяет координаты на предмет соприкосновения
        :return: True, если нижняя часть coords1 соприкасается с верхней частью coords2. False в любом другом случае.
        """
        # Проверка координат по x и y
        if (((coords2[0] <= coords1[0] <= coords2[2]) or (coords2[0] <= coords1[2] <= coords2[2]))  # По x
            and
            ((coords2[1] <= coords1[1] <= coords2[3]) or (coords2[1] <= coords1[3] <= coords2[3]))):  # По y
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

