import tkinter as tk
from tkinter import ttk
import meteo as met
import info as inf

def main():
    
    # ----- Finestra principale -----
    
    root = tk.Tk()
    root.title("Meteo app Main")
    root.geometry("320x180")

    # ----- ON/OFF dei pulsanti -----
    
    def disabilita_opzioni():
        btn_op1.config(state=tk.DISABLED)
        
    def disabilita_info():
        btn_info.config(state=tk.DISABLED)

    def abilita_opzioni():
        btn_op1.config(state=tk.NORMAL)
    
    def abilita_info():
        btn_info.config(state=tk.NORMAL)
        
    # ----- Gestione schermata ----
    
    def apri_schermata(opz):
        
        disabilita_opzioni()
        win = None
        
        if opz == 1:
            win = met.meteo_window(root)

        if win is not None:
            try:
                root.wait_window(win)
            except tk.TclError:
                pass

        try:
            abilita_opzioni()
        except tk.TclError:
            pass
    
    def apri_info():
        win = None
        disabilita_info()
        win = inf.main(root)
        if win is not None:
            root.wait_window(win)
        abilita_info()

    # ----- Gestione pulsanti -----
    
    def opzione_1():
        apri_schermata(1)
        
    def opzione_5():
        apri_info()

    def esci():
        root.destroy()
    
    # ----- Finestra principale -----
    
    frame = ttk.Frame(root, padding=12)
    frame.pack(expand=True, fill=tk.BOTH)

    # ----- PULSANTI -----
    
    btn_op1 = ttk.Button(frame, text="Meteo", command=opzione_1)
    btn_op1.grid(row=0, column=0, columnspan=3, pady=(12, 0), sticky="ew")

    btn_info = ttk.Button(frame, text="Info", command=opzione_5)
    btn_info.grid(row=2, column=0, columnspan=3, pady=(12, 0), sticky="ew")

    btn_esci = ttk.Button(frame, text="Esci", command=esci)
    btn_esci.grid(row=3, column=0, columnspan=3, pady=(12, 0), sticky="ew")
   
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    import multiprocessing
    import sys
    
    # On Windows calling this function is necessary.
    multiprocessing.freeze_support()

    # ----- Prevenzione riesecuzione -----
    if getattr(sys, 'frozen', False):
        multiprocessing.set_executable(sys.executable)

    main()
