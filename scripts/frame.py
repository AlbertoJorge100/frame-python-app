import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from pdf import (
    processPdf, createTextFile, renameFiles, getMessage, getErrorsCounter, reset
)

TitleApp = "Proceso de Archivos"
Input = None
Directory = None
Directory2 = None
Window = None
LoginWindow = None
Label = None
MessageLabel = \
    "Presione \"Seleccionar Directorio\" para abrir una carpeta\n y despues presione \"Procesar\""
StartTime = None
TimeLabel = None
Running = False
DirButton = None
Dir2Button = None
ProcessButton = None
CmbOptions = None
CmbArray = ["Renombrar PDF's", "Procesar Liquidaciones", "Procesar Créditos Fiscales"]
Option = 1

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

def selectDirectory(option):    
    global Directory, Directory2, Label    
    Window.update_idletasks()    
    directory = filedialog.askdirectory(parent=Window, title="Seleccionar Directorio")
    if not directory: return
    if option == 1: Directory = directory
    else: Directory2 = directory
    Label.config(text=f"{MessageLabel}\n- {Directory}\n- {Directory2}")

def processOptions(event):
    global Option, Directory, Directory2
    #Directory = Directory2 = ""
    Option = 1 if CmbOptions.get() == CmbArray[0] else \
        2 if CmbOptions.get() == CmbArray[1] else 3
    Dir2Button.config(state= tk.DISABLED if Option == 1 else tk.ACTIVE)    

def process():        
    global MessageLabel
    if not Directory:
        return showAlert(f'No ha seleccionado una carpeta ', 2)
    if Option == 2 and not Directory2:
        return showAlert(f'No ha seleccionado una carpeta para crear el archivo de texto', 2)
    if not messagebox.askyesno('Confirmación', '¿Esta seguro de procesar los archivos?'):
        return
    MessageLabel = f"Procesando archivos por favor espere. \n- {Directory}\n- {Directory2}"
    Label.config(text=MessageLabel)    
    threading.Thread(target=runProcess, daemon=True).start()        

def runProcess():
    global StartTime, Running, ProcessButton, DirButton, MessageLabel
    try:
        StartTime = time.time()
        Running = True
        ProcessButton.config(state=tk.DISABLED)
        DirButton.config(state=tk.DISABLED)
        Dir2Button.config(state=tk.DISABLED)
        updateTimer()
        processPdf(Option, Directory)
        if Option == 1: renameFiles()
        else: createTextFile(Directory2)
        Running = False
        message = getMessage()
        MessageLabel = f"¡Proceso completado! \n{message}"
        Label.config(text=MessageLabel)
        if getErrorsCounter() == 0:
            return messagebox.showinfo(f"{CmbOptions.get()}", message)            
        messagebox.showerror(f"{CmbOptions.get()} Error", message)    
    except Exception as e:
        messagebox.showerror(f"Error principal: {str(e)}")
    finally:
        ProcessButton.config(state=tk.NORMAL)
        DirButton.config(state=tk.NORMAL)
        if Option == 2: Dir2Button.config(state=tk.NORMAL)
        reset()

def validateUser():
    text = Input.get()
    if text == '' or text != "230498": 
        Input.delete(0, tk.END)
        return messagebox.showerror('Error', "Contraseña erronea")
    LoginWindow.destroy()
    frame()

def login():
    global Input, LoginWindow
    # Crear LoginWindow
    LoginWindow = tk.Tk()
    LoginWindow.title(TitleApp)    
    LoginWindow.resizable(False, False)
    #LoginWindow.iconbitmap('icon.ico')
    windowWidth = 300
    windowHeigth = 200
    screenWidth = LoginWindow.winfo_screenwidth()
    screenHeight = LoginWindow.winfo_screenheight()
    pos_x = (screenWidth // 2) - (windowWidth // 2)
    pos_y = (screenHeight // 2) - (windowHeigth // 2)
    LoginWindow.geometry(f"{windowWidth}x{windowHeigth}+{pos_x}+{pos_y}")
    Input = ttk.Entry(LoginWindow, width=30, show="*")
    Input.pack(pady=40)
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)    
    style.configure("TEntry", font=("Arial", 10, "bold"), padding=5)    
    button = ttk.Button(LoginWindow, text="Ingresar", command=validateUser)
    button.pack(pady=0)    
    LoginWindow.mainloop()

def frame():    
    global Label, Window, TimeLabel, DirButton, Dir2Button, ProcessButton, CmbOptions
    Window = tk.Tk()
    Window.title(TitleApp)
    #Window.iconbitmap('icon.ico')
    #Window.resizable(False, False)
    windowWidth = 500
    windowHeigth = 400
    screenWidth = Window.winfo_screenwidth()
    screenHeight = Window.winfo_screenheight()
    pos_x = (screenWidth // 2) - (windowWidth // 2)
    pos_y = (screenHeight // 2) - (windowHeigth // 2)
    Window.geometry(f"{windowWidth}x{windowHeigth}+{pos_x}+{pos_y}")
    Label = tk.Label(
        Window, 
        text=MessageLabel, 
        font=("Arial", 9)
    )
    TimeLabel = tk.Label(Window, text="Tiempo transcurrido: 00:00", font=("Arial", 10))
    TimeLabel.pack(pady=5)
    Label.pack(pady=20)
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10), padding=5)    
    style.configure("TCombobox", font=("Arial", 10), padding=5)    
    CmbOptions = ttk.Combobox(
        Window, 
        values=CmbArray, 
        state="readonly"
    )
    CmbOptions.set(CmbArray[0])
    CmbOptions.pack(pady=10)
    CmbOptions.bind("<<ComboboxSelected>>", processOptions)
    frame = tk.Frame(Window)
    frame.pack(pady=10)
    DirButton = ttk.Button(frame, text="Seleccionar Directorio", command=lambda:selectDirectory(1))
    DirButton.grid(row=0, column=0, padx=10)
    Dir2Button = ttk.Button(frame, text="Seleccionar Directorio", state=tk.DISABLED, command=lambda:selectDirectory(2))
    Dir2Button.grid(row=0, column=1, padx=10)
    ProcessButton = ttk.Button(Window, text="Procesar", command=process)
    ProcessButton.pack(pady=10)
    Window.mainloop()

if __name__ == "__main__":    
    #frame()
    login()