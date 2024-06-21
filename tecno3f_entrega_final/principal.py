import tkinter as tk
from usuario.vista import Frame, barrita_menu

def main():
    ventana = tk.Tk()
    ventana.title('Gestor de Stock')
    ventana.resizable(0, 0)

    barrita_menu(ventana)
    app = Frame(root=ventana)

    ventana.mainloop()

if __name__ == '__main__':
    main()
