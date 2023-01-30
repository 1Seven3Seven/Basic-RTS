# ToDo: UI Time
# ToDo: Map creating tool
#   Add in a way of storing a var reference, name, min, max and increment for the ui
# ToDo: Create a save format for maps that is easily upgradable

import tkinter as tk
from tkinter import ttk


def main():
    window = tk.Tk()
    window.title("Map creation tool")
    window.geometry("500x500")

    # Dropdown box for the generators
    # Somehow look into the classes for the parameters that can change and add in those options.

    combo = ttk.Combobox(window)
    combo['values'] = [1, 2, 3, 4, 5]
    combo.current(0)
    combo.pack()

    spin = tk.Spinbox(window, from_=0.0, to=1, increment=0.01, width=5)
    spin.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
