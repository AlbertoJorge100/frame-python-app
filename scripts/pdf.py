import pdfplumber
import re
import os

#Código de Generación - Número de Control
MatchText = "Número de Control"
Directory = None
ListFiles = []
ErrorsMessage = ""
ErrorsNumber = 0
Message = ""
FilesNumber = 0
RenamedNumber = 0

#type: 1 success, 2 error
def setMessage(message, type = 1):
    global Message, ErrorsMessage, ErrorsNumber
    if type == 1:
        Message += f"{message}\n"
    else: 
        ErrorsMessage += f"{message}\n"
        ErrorsNumber += 1

def getErrorsCounter():
    return ErrorsNumber

def getMessage():
    setMessage(f"Archivos PDF procesados: {len(ListFiles)}/{FilesNumber}")
    setMessage(f"Archivos PDF renombrados: {RenamedNumber}/{FilesNumber}")
    return f"{Message} \n \
        {'' if ErrorsNumber == 0 else \
        f"{ErrorsNumber} errores encontrados:\n{ErrorsMessage}"}"

def findText(fileName):
    try:
        with pdfplumber.open(os.path.join(Directory, fileName)) as pdf:
            pageNumber = 0        
            text = pdf.pages[pageNumber].extract_text()
            result = re.search(rf"{MatchText}:\s*([^\s]+)", text)
            if result: return result.group(1)
        return None            
    except Exception as e:
        setMessage(f"error {fileName}: {str(e)}", 2)
    except FileNotFoundError as e:        
        setMessage(f"No encontrado \"{fileName}\": {str(e)}", 2)
    except OSError as e:
        setMessage(f"error {fileName}: {str(e)}", 2)        
    except pdfplumber.utils.PDFPageCountError as e:
        setMessage(f"error {fileName}: {str(e)}", 2)
    except AttributeError as e:
        setMessage(f"error {fileName}: {str(e)}", 2)
    except ValueError as e:
        setMessage(f"error {fileName}: {str(e)}", 2)

def processPdf(directory):
    try:
        global FilesNumber, Directory
        Directory = directory
        for fileName in os.listdir(Directory): 
            FilesNumber += 1           
            try:
                if not fileName.lower().endswith(".pdf"): continue
                code = findText(fileName)
                if code: ListFiles.append({"file": fileName, "code": code})
                else: setMessage(f"No se pudo obtener el código del archivo: {fileName}", 2)
            except Exception as e:
                setMessage(f"error {fileName}: {str(e)}", 2)
    except Exception as e:
        setMessage(f"error al procesar los archivos: {str(e)}", 2)

def renameFiles():
    try:
        global RenamedNumber
        for file in ListFiles:
            try:
                os.rename(os.path.join(Directory, file['file']), os.path.join(Directory, f"{file['code']}.pdf"))
                RenamedNumber += 1
            except FileExistsError as e:
                setMessage(f"archivo {file['file']} duplicado: {str(e)}", 2)
            except Exception as e:
                setMessage(f"error {file['file']}: {str(e)}", 2)
            except OSError as e:
                setMessage(f"error {file['file']}: {str(e)}", 2)
            except AttributeError as e:
                setMessage(f"error {file['file']}: {str(e)}", 2)
            except ValueError as e:
                setMessage(f"error {file['file']}: {str(e)}", 2)            
    except Exception as e:
        setMessage(f"error al renombrar los archivos: {str(e)}", 2)
    
