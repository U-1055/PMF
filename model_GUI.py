import tkinter
from tkinter import Tk, Button, Toplevel, Frame
import model as mdl
from physics_objects import Vector
from threading import Thread
import time


class TestWindow(Toplevel):
    model: mdl.Model

    def __init__(self, model_: mdl.Model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model_
        self.__place_widgets()

    def __place_widgets(self):
        main_frm = Frame(self)
        main_frm.pack(fill=tkinter.BOTH, expand=True)

        st_btn = Button(main_frm, text='Начать обработку', command=self.model.start_processing)
        st_btn.grid(row=0, column=0)

        stp_btn = Button(main_frm, text='Прервать обработку', command=self.model.stop_processing)
        stp_btn.grid(row=0, column=1)

        plot_btn = Button(main_frm, text='Получить данные об объектах', command=self.__plot_data)
        plot_btn.grid(row=0, column=2)

    def __plot_data(self):
        for obj in self.model._objects:
            if isinstance(obj, mdl.MoveableObject):
                obj.plot_data()


if __name__ == '__main__':
    root = Tk()
    width = root.winfo_screenwidth() // 2
    height = root.winfo_screenheight() // 2
    root.geometry(f"{width}x{height}+{width // 2}+{height // 2}")
    root.title('Тестирование модели')

    model = mdl.Model(model_size=(width, height), resistance=0, tick=0.001)
    model.place(x=0, y=0, width=width, height=height)


    add_btn = Button(model, command=lambda: model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 1, width // 2 + 25, 25)))
    add_btn.pack()

    model.add_object(mdl.Object, model.create_rectangle(0, height, width, height + 1, fill='Black'), 2)

    a = model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 0, width // 2 + 100, 100), weight=2)
    b = model.add_object(mdl.MoveableObject, model.create_oval(width // 2 - 50, 0, width // 2 - 25, 100), weight=1)
    c = model.add_object(mdl.MoveableObject, model.create_oval(width // 2 + 150, 0, width // 2 + 175, 100), weight=5)

  #  root.after(100, lambda : a.forces.clear())
   # root.after(100, lambda: a.forces.append(Vector(1, -1)))
  #  root.after(101, lambda: a.forces.clear())

    window = TestWindow(model)
    window.geometry(f'500x500')

    root.mainloop()

