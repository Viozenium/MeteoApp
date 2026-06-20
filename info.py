"""Finestra "Info / About" dell'applicazione.

I colori seguono il tema attivo nella finestra principale (vedi themes.py),
così l'aspetto resta coerente con il resto dell'app.
"""

import tkinter as tk
import webbrowser

from themes import THEMES

AUTHOR = "Mizu"
VERSION = "2.0.0"
GITHUB_LABEL = "Viozenium"
GITHUB_URL = "https://github.com/Viozenium"


def _darken(hex_color, factor=0.85):
    """Scurisce leggermente un colore esadecimale (usato per l'hover del bottone)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, int(c * factor)) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def show_info_window(parent, theme_name="scuro"):
    """Apre la finestra Info come Toplevel modale di `parent`, colorata secondo il tema attivo."""
    colors = THEMES.get(theme_name, THEMES["scuro"])
    bg = colors["bg"]
    fg = colors["fg"]
    divider = colors["panel_bg"]
    highlight = colors["accent"]
    highlight_fg = colors["accent_fg"]
    muted = colors["muted"]

    info_win = tk.Toplevel(parent)
    info_win.title("Info")
    info_win.geometry("360x260")
    info_win.resizable(False, False)
    info_win.configure(bg=bg)
    info_win.transient(parent)
    info_win.grab_set()

    def close():
        info_win.grab_release()
        info_win.destroy()

    info_win.protocol("WM_DELETE_WINDOW", close)

    tk.Frame(info_win, bg=highlight, height=3).pack(fill="x")
    hdr = tk.Frame(info_win, bg=bg, padx=28, pady=18)
    hdr.pack(fill="x")
    tk.Label(
        hdr, text="◈  ABOUT", font=("Courier New", 16, "bold"), bg=bg, fg=highlight
    ).pack(anchor="w")

    tk.Frame(info_win, bg=divider, height=1).pack(fill="x", padx=28)

    body = tk.Frame(info_win, bg=bg, padx=28, pady=20)
    body.pack(fill="both", expand=True)

    def row(label, value):
        f = tk.Frame(body, bg=bg)
        f.pack(fill="x", pady=5)
        tk.Label(
            f,
            text=label,
            font=("Courier New", 10),
            bg=bg,
            fg=muted,
            width=10,
            anchor="w",
        ).pack(side="left")
        tk.Label(
            f, text=value, font=("Courier New", 10, "bold"), bg=bg, fg=fg, anchor="w"
        ).pack(side="left")

    row("Author", AUTHOR)
    row("Version", VERSION)

    f = tk.Frame(body, bg=bg)
    f.pack(fill="x", pady=5)
    tk.Label(
        f,
        text="GitHub",
        font=("Courier New", 10),
        bg=bg,
        fg=muted,
        width=10,
        anchor="w",
    ).pack(side="left")
    link = tk.Label(
        f,
        text=GITHUB_LABEL,
        font=("Courier New", 10, "bold"),
        bg=bg,
        fg=highlight,
        cursor="hand2",
        anchor="w",
    )
    link.pack(side="left")
    link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))
    link.bind("<Enter>", lambda e: link.config(fg=fg))
    link.bind("<Leave>", lambda e: link.config(fg=highlight))

    tk.Frame(info_win, bg=divider, height=1).pack(fill="x")
    tk.Button(
        info_win,
        text="Chiudi",
        font=("Courier New", 10, "bold"),
        bg=highlight,
        fg=highlight_fg,
        activebackground=_darken(highlight),
        activeforeground=highlight_fg,
        relief="flat",
        bd=0,
        padx=20,
        pady=8,
        command=close,
    ).pack(pady=12)

    return info_win


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_info_window(root, theme_name="scuro")
    root.mainloop()
