import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from pdf import (
    processPdf, renameFiles, getMessage, getErrorsCounter
)

Directory = None
Window = None
Label = None
StartTime = None
TimeLabel = None
Running = False
DirButton = None
ProcessButton = None

def updateTimer():
    if not Running: return
    elapsed_time = time.time() - StartTime
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    TimeLabel.config(text=f"Tiempo transcurrido: {minutes:02}:{seconds:02}")
    Window.after(1000, updateTimer)  # Actualiza cada segundo

def showAlert(message, type = 1):
    if type == 1: 
        return messagebox.showinfo("Confirmación", message)
    messagebox.showerror("Error", message)

def cerrar():
    Window.destroy()

def selectDirectory():
    global Directory, Label
    Window.update_idletasks()    
    directory = filedialog.askdirectory(parent=Window, title="Seleccionar Directorio")
    if not directory: return
    Directory = directory
    Label.config(text=f"{directory}")

def process():    
    if not Directory:
        return showAlert('No ha seleccionado una carpeta', 2)
    if not messagebox.askyesno('Confirmación', '¿Esta seguro de procesar los archivos?'):
        return
    Label.config(text=f"Procesando archivos en:\n \"{Directory}\"\n\nPor favor espere...")    
    threading.Thread(target=runProcess, daemon=True).start()        

def runProcess():
    global StartTime, Running, ProcessButton, DirButton
    try:
        StartTime = time.time()
        Running = True
        ProcessButton.config(state=tk.DISABLED)
        DirButton.config(state=tk.DISABLED)
        updateTimer()
        processPdf(Directory)
        renameFiles()
        Running = False
        message = getMessage()
        Label.config(text=f"¡Proceso completado! \n{message}")
        if getErrorsCounter() == 0:
            return messagebox.showinfo('Confirmación', message)            
        messagebox.showerror('Error', message)    
    except Exception as e:
        messagebox.showerror(f"Error principal: {str(e)}")
    finally:
        ProcessButton.config(state=tk.NORMAL)
        DirButton.config(state=tk.NORMAL)

def frame():    
    global Label, Window, TimeLabel, DirButton, ProcessButton
    Window = tk.Tk()
    Window.title("Renombrar Archivos")
    #Window.resizable(False, False)
    windowWidth = 500
    windowHeigth = 300
    screenWidth = Window.winfo_screenwidth()
    screenHeight = Window.winfo_screenheight()
    pos_x = (screenWidth // 2) - (windowWidth // 2)
    pos_y = (screenHeight // 2) - (windowHeigth // 2)
    Window.geometry(f"{windowWidth}x{windowHeigth}+{pos_x}+{pos_y}")
    Label = tk.Label(
        Window, 
        text="Presione \"Seleccionar Directorio\" para abrir una carpeta\n y despues presione \"Procesar\"", 
        font=("Arial", 9)
    )
    TimeLabel = tk.Label(Window, text="Tiempo transcurrido: 00:00", font=("Arial", 10))
    TimeLabel.pack(pady=5)
    Label.pack(pady=20)
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)
    DirButton = ttk.Button(Window, text="Seleccionar Directorio", command=selectDirectory)
    DirButton.pack(pady=10)
    ProcessButton = ttk.Button(Window, text="Procesar", command=process)
    ProcessButton.pack(pady=10)
    Window.mainloop()

if __name__ == "__main__":    
    frame()