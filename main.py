import tkinter as tk
from widgets import ModelController


class Window(tk.Frame):

    def __init__(self, window_size: tuple[int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_size = window_size
        self.__place_widgets()

    def __place_widgets(self):
        model_controller = ModelController(master=self, window_size=(self.window_size[0] // 2, self.window_size[1] // 2), bg='Black')
        model_controller.place(x=0, y=0, width=self.window_size[0] // 2, height=self.window_size[1] // 2)

def launch():
    root = tk.Tk()
    width = 1000
    height = 750
    root.geometry("1000x750+460+180")
    root.title('Title')

    window = Window(master=root, window_size=(width, height))
    window.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == '__main__':
    launch()
