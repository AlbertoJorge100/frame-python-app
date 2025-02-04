import pdfplumber
from datetime import datetime
import re
import os

#Código de Generación - Número de Control
ListFiles = []
Strings = ""
Directory = None
BaseMatches = [
    "Código de Generación", "Número de Control", "Sello de Recepción"
]
MatchTexts = []
for i in BaseMatches: MatchTexts.append(i)
# Liquidations
Texts2 = [
    "IVA de las operaciones a liquidar",
    "Montos sujetos a percepción sin IVA",
    "IVA percibido (2%)"
]
# CC's
Texts3 = [
    "Sumatoria de ventas", 
    "Impuesto al Valor Agregado 13%",
    "Total a Pagar"
]
ErrorsMessage = ""
Message = ""
ErrorsNumber = 0
FilesNumber = 0
ProcessedNumber = 0
RenamedNumber = 0
#1 rename, 2 liquidations, 3 CC's
ProcessOption = 1

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
    isFirstOption = ProcessOption == 1
    setMessage(f"Archivos PDF procesados: {len(ListFiles) if isFirstOption else ProcessedNumber}/{FilesNumber}")
    if isFirstOption: setMessage(f"Archivos PDF renombrados: {RenamedNumber}/{FilesNumber}")
    return f"{Message} \n \
        {'' if ErrorsNumber == 0 else \
        f"{ErrorsNumber} errores encontrados:\n{ErrorsMessage}"}"

def reset():
    global Message, ErrorsMessage, Strings, ErrorsNumber, \
        FilesNumber, ProcessedNumber, RenamedNumber, ListFiles, MatchTexts 
    Message = ErrorsMessage = Strings = ""    
    ErrorsNumber = FilesNumber = ProcessedNumber = RenamedNumber = 0
    ListFiles = []
    MatchTexts = []
    for i in BaseMatches: MatchTexts.append(i)    

def spaces(text):    
    if ProcessOption == 2:
        if text == MatchTexts[0]:
            return '               '
        elif text == MatchTexts[1]:
            return '                  '
        elif text == MatchTexts[2]:
            return '                 '
        elif text == MatchTexts[3]:
            return '  '
        elif text == MatchTexts[4]:
            return ''
        elif text == MatchTexts[5]:
            return '        	     '
    else:
        if text == MatchTexts[0]:
            return ' '
        elif text == MatchTexts[1]:
            return '    '
        elif text == MatchTexts[2]:
            return '   '
        elif text == MatchTexts[3]:
            return '  '
        elif text == MatchTexts[4]:
            return '	       '
        elif text == MatchTexts[5]:
            return '	       '

def findText(fileName):
    string=""
    dte="------------------------------------------------------------------------------\n\n"\
        f"DTE: {"                                " if ProcessOption == 2 else "                  "}"
    try:
        with pdfplumber.open(os.path.join(Directory, fileName)) as pdf:
            for page in pdf.pages:
                for text in MatchTexts:                    
                    result = re.search(rf"{re.escape(text)}:\s*([^\s]+)", page.extract_text())
                    if result:
                        if ProcessOption == 1: return result.group(1)
                        if (text == MatchTexts[1]):
                            dte+=f"{re.search(r'0+(\d+)$', result.group(1)).group(1)}"
                        string+=f"{"IVA 13%" if ProcessOption == 3 and text == MatchTexts[4] else text}: {spaces(text)}{result.group(1)}\n"
                        continue
        return None if ProcessOption == 1 else f"{dte}\n{string}\n"
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

def processPdf(option, directory):
    try:
        global FilesNumber, Directory, ProcessOption, MatchTexts, Strings, ProcessedNumber
        Directory = directory
        ProcessOption = option
        isFirstOption = ProcessOption == 1
        if(isFirstOption):
            MatchTexts = [MatchTexts[1]]
        else: MatchTexts.extend(Texts2 if ProcessOption == 2 else Texts3)
        for fileName in os.listdir(Directory): 
            FilesNumber += 1           
            try:
                if not fileName.lower().endswith(".pdf"): continue
                result = findText(fileName)
                if not result or result == "": 
                    setMessage(f"No se pudo obtener el resultado del archivo: {fileName}", 2)
                if isFirstOption: 
                    ListFiles.append({"file": fileName, "code": result})
                    continue
                ProcessedNumber += 1
                Strings += result
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
    
def createTextFile(directory):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = date.replace(' ', '_').replace(':', '_').replace('-', '_')
    fileName = f"{'liquidaciones_' if ProcessOption == 2 else 'creditos_fiscales'}_{date}.txt"    
    with open(os.path.join(directory, fileName), "a", encoding="utf-8") as file:
        file.write(
            f"{"LIQUIDACIONES" if ProcessOption == 2 else "CREDITOS FISCALES"} {ProcessedNumber}/{FilesNumber}\n\n{Strings}"
        )    