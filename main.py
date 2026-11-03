import tkinter as tk
import logging
from dotenv import load_dotenv
from interfaz.aplicacion import EcoTechApp

load_dotenv()

logging.basicConfig(
    filename='ecotech.log',
    filemode='a',
    level=logging.ERROR,
    format='%(asctime)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s'
)

def main():
    root = tk.Tk()
    EcoTechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
