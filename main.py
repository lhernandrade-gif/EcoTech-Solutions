import tkinter as tk

from interfaz.aplicacion import EcoTechApp


def main():
    root = tk.Tk()
    EcoTechApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
