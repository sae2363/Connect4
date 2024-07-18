import tkinter
from tkinter import ttk

class GUI:
    def __init__(self) -> None:
        pass

    m = tkinter.Tk()

    '''
    widgets are added here
    '''

    frm = ttk.Frame(m, padding=10)
    frm.grid()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=m.destroy).grid(column=1, row=0)

    # Test to make sure Tkinter works

    m.mainloop()