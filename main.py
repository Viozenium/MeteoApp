"""Punto di ingresso della Meteo App."""

import tkinter as tk

import config
from ui import MeteoApp


def meteo_window(parent, standalone=False):
    """
    Crea la finestra Meteo come Toplevel di `parent`.
    Se standalone=True, alla chiusura viene chiusa anche `parent`
    (evita che il processo Python resti "fantasma" in console
    quando questo script viene eseguito da solo).
    """
    win = tk.Toplevel(parent)
    win.title("Meteo App")
    win.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    win.minsize(680, 480)

    MeteoApp(win)

    def on_close():
        win.destroy()
        if standalone:
            parent.quit()
            parent.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)
    return win


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    win = meteo_window(app, standalone=True)
    app.mainloop()
