import tkinter as tk
from model import Model, Object, MoveableObject


class BaseCounter(tk.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PBCounter(tk.Label):
    
    def __init__(self):
        super().__init__()


class ModelController(tk.Frame):
    """Контроллер модели. Управляет самой моделью и счётчиками."""
    model: Model

    def __init__(self, window_size: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_width = window_size[0] // 2
        model_height = window_size[1]
        self.model = Model(master=self, model_size=(model_width, model_height))
        self.model.place(x=0, y=0, width=model_width, height=model_height)
        self.model.add_object(Object, self.model.create_rectangle(model_width - 150, model_height - 25, model_width, model_height, fill='Black'))
        self.model.add_object(MoveableObject, self.model.create_oval(model_width // 2, 0, model_width // 2 + 5, 5, fill='Black'))

        self.model.add_object(MoveableObject, self.model.create_arc(model_width // 3, 25, model_width // 3 + 10, 10))
        self.model.add_object(MoveableObject,
                              self.model.create_oval(model_width // 4, 0, model_width // 4 + 5, 5, fill='Black'))
        self.model.add_object(MoveableObject,
                              self.model.create_oval(model_width // 6, 0, model_width // 6 + 5, 5, fill='Black'))
        self.model.add_object(MoveableObject,
                              self.model.create_oval(model_width // 8, 0, model_width // 8 + 5, 5, fill='Black'))