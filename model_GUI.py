from tkinter import Tk, Frame
import model as mdl

if __name__ == '__main__':
    root = Tk()
    width = root.winfo_screenwidth() // 2
    height = root.winfo_screenheight() // 2
    root.geometry(f"{width}x{height}+{width // 2}+{height // 2}")
    root.title('Тестирование модели')

    model = mdl.Model(model_size=(width, height))
    model.place(x=0, y=0, width=width, height=height)
    model.add_object(mdl.Object, model.create_rectangle(0, height, width, height, fill='Black'))

    model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 1, width // 2 + 25, 25))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 25, width // 2 + 50, 50))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 50, width // 2 + 75, 75))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2, 75, width // 2 + 100, 100))

    model.add_object(mdl.MoveableObject, model.create_oval(width // 2 + 60, 1, width // 2 + 75, 25))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2 + 90, 1, width // 2 + 115, 25))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2 - 30, 1, width // 2 - 5, 25))
    model.add_object(mdl.MoveableObject, model.create_oval(width // 2 - 60, 1, width // 2 - 35, 25))

    root.mainloop()
