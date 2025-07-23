import datetime
import tkinter
from tkinter import Tk, Button, Toplevel, Frame, Label, StringVar, LabelFrame, W, E, N, S
import model as mdl
from physics_objects import Vector, Force
from threading import Thread
import time
from base import plu_g, jup_g, sun_g, g


def force_(obj):
    obj.forces.add(Vector(-1000, -5000))
    root.after(2, lambda: obj.forces.pop())


class StopWatch(Label):
    __start_line = 'Время:'
    __end_line = 'мс'

    def __init__(self, start_time: int = 0, step: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if step <= 0:
            raise ValueError(f'Step must be > 0, but step = {step}')

        self.__counting = False
        self.__time = start_time
        self.__step = step

        self.configure(text=f'{self.__start_line} {self.__time} {self.__end_line}')

    def start(self):
        self.__counting = True
        root.after(self.__step, self.__update_stopwatch)

    def stop(self):
        self.__counting = False

    def __update_stopwatch(self):
        if not self.__counting:
            return

        self.__time += 1
        self.configure(text=f'{self.__start_line} {self.__time} {self.__end_line}')
        root.after(self.__step, self.__update_stopwatch)


class TestWindow(Toplevel):
    model: mdl.Model

    def __init__(self, model_: mdl.Model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model_
        self.__place_widgets()

    def __place_widgets(self):
        main_frm = Frame(self)
        main_frm.pack(fill=tkinter.BOTH, expand=True)

        st_btn = Button(main_frm, text='Начать обработку', command=self.start)
        st_btn.grid(row=0, column=0)

        stp_btn = Button(main_frm, text='Прервать обработку', command=self.stop)
        stp_btn.grid(row=0, column=1)

        plot_btn = Button(main_frm, text='Получить данные об объектах', command=self.__plot_data)
        plot_btn.grid(row=0, column=2)

        #информационное поле
        info_frm = LabelFrame(main_frm, text='Информация о сцене')
        info_frm.grid(row=1, column=0, columns=3, sticky=W + E + N + S)

        lbl_objects_num = Label(info_frm, text=f'Объектов: {len(self.model.objects)}')
        lbl_objects_num.grid(row=0, column=0)

        self.__lbl_stopwatch = StopWatch(master=info_frm)
        self.__lbl_stopwatch.grid(row=0, column=1)

        objects_frm = LabelFrame(info_frm, text='Информация об объектах')  # ToDo: сделать treeview для отображения информации об объектах

    def start(self):
        self.model.start_processing()
        self.__lbl_stopwatch.start()

    def stop(self):
        self.model.stop_processing()
        self.__lbl_stopwatch.stop()

    def __plot_data(self):
        for obj in self.model.objects:
            if isinstance(obj, mdl.MoveableObject):
                obj.plot_data()


if __name__ == '__main__':
    root = Tk()
    width = root.winfo_screenwidth() // 2
    height = root.winfo_screenheight() // 2
    root.geometry(f"{width}x{height}+{width // 2}+{height // 2}")
    root.title('Тестирование модели')

    model = mdl.Model(model_size=(width, height), tick=0.001, resistance=Vector(0, 0), gravity_acceleration=plu_g)
    model.place(x=0, y=0, width=width, height=height)

    model.add_object(mdl.Object, model.create_rectangle(0, height-10, width, height), 1)
    model.add_object(mdl.Object, model.create_rectangle(0, 0, width, 25, fill='Black'), 1)
    model.add_object(mdl.Object, model.create_rectangle(width - 25, 0, width, height, fill='Black'), 1)
    model.add_object(mdl.Object, model.create_rectangle(0, 0, 25, height, fill='Black'), 1)

    a = model.add_object(mdl.MoveableObject, model.create_rectangle(50, 50, 100, 75), weight=1)
    b = model.add_object(mdl.MoveableObject, model.create_rectangle((width - 100, 50, width // 2 + 100, 150)), weight=1)
    c = model.add_object(mdl.MoveableObject, model.create_rectangle((55, 100, 75, 149)), weight=1)
    model.add_object(mdl.MoveableObject, model.create_rectangle(width - 102, 25, width // 2 + 102, 49), weight=1)

   # c.forces.add(Vector(-1, -5))

    window = TestWindow(model)
    window.geometry(f'500x500')

    root.mainloop()

