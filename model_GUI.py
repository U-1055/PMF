import tkinter
from tkinter import Tk, Button, Toplevel, Frame
import model as mdl
from physics_objects import Vector, Force
from threading import Thread
import time
from base import plu_g, jup_g, sun_g


def force_(obj):
    obj.forces.add(Vector(-1000, -5000))
    root.after(2, lambda: obj.forces.pop())


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

        stp_btn = Button(main_frm, text='Прервать обработку', command=self.model.stop_processing)
        stp_btn.grid(row=0, column=1)

        plot_btn = Button(main_frm, text='Получить данные об объектах', command=self.__plot_data)
        plot_btn.grid(row=0, column=2)

    def start(self):
        self.model.start_processing()

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

    model = mdl.Model(model_size=(width, height), resistance=Vector(0, 0), tick=0.001, gravity_acceleration=plu_g)
    model.place(x=0, y=0, width=width, height=height)

    model.add_object(mdl.Object, model.create_rectangle(0, 100, width, height), 1)
    model.add_object(mdl.Object, model.create_rectangle(0, 0, width, 1, fill='Black'), 1)

    a = model.add_object(mdl.MoveableObject, model.create_rectangle(width // 2, 50, width // 2 + 100, 75), weight=1)

    window = TestWindow(model)
    window.geometry(f'500x500')

    root.mainloop()

