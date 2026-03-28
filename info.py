import tkinter as tk
import webbrowser
import sys

def main(parent=None, standalone=False):
    # se standalone, la finestra principale è il Tk
    if standalone or parent is None:
        info_win = tk.Tk()
    else:
        info_win = tk.Toplevel(parent)

    info_win.title("Info")
    info_win.geometry("320x220")
    info_win.resizable(False, False)

    def on_close():
        info_win.destroy()
        if standalone:
            info_win.quit()  # necessario se Tk è la finestra principale

    info_win.protocol("WM_DELETE_WINDOW", on_close)

    container = tk.Frame(info_win, padx=30, pady=15)
    container.pack(expand=True, fill="both")

    title_font = ("Segoe UI", 16, "bold")
    text_font = ("Segoe UI", 11)
    link_font = ("Segoe UI", 11, "underline")

    tk.Label(container, text="ABOUT", font=title_font).pack(pady=(0, 20))
    tk.Frame(container, height=2, bd=1, relief="sunken").pack(fill="x", pady=15)
    tk.Label(container, text="Author: Mizu", font=text_font).pack(pady=2)
    tk.Label(container, text="Ver: 1.0", font=text_font).pack(pady=2)
    git_label = tk.Label(container, text="GitHub: Viozenium", font=link_font, fg="blue", cursor="hand2")
    git_label.pack(pady=4)
    git_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Viozenium"))

    return info_win

# ----- Stand-alone -----
def _standalone():
    info_win = main(standalone=True)
    info_win.mainloop()

if __name__ == "__main__" and not getattr(sys, 'frozen', False):
    _standalone()
