import pandas as pd
import os
from datetime import datetime

ErrorsMessage = ""
Message = ""
ErrorsNumber = 0

#type: 1 success, 2 error
def setMessage(message, type = 1):
    global Message, ErrorsMessage, ErrorsNumber
    if type == 1:
        Message += f"{message}\n"
    else: 
        ErrorsMessage += f"- {message}\n"
        ErrorsNumber += 1

def getErrorsCounterExcel():
    global ErrorsNumber
    number = ErrorsNumber
    ErrorsNumber = 0    
    return number

def getMessageExcel():    
    global Message, ErrorsMessage
    setMessage(f"Archivo ordenado:")
    message = (
        f"{Message} \n"
        '' if ErrorsNumber == 0 else f"{ErrorsNumber} errores encontrados:\n{ErrorsMessage}"
    )
    Message = ErrorsMessage = ""    
    return message

#option: 1 retención de IVA, NC. 2 libro de compras
def readFile(file, option):
    global ErrorsNumber
    data = []
    try:        
        df = pd.read_excel(file, header=None)
        for index, row in df.iterrows():
            if option == 1 and row[14] < 0: 
                data.append([
                    row[0],
                    "",
                    row[4],
                    row[1].strftime("%d/%m/%Y"),
                    "",
                    "",
                    "",
                    row[2],                    
                    row[5],
                    row[8] * -1,
                    row[14] * -1,
                ])
            elif option == 2:
                data.append([
                    row[1],
                    row[22],
                    row[23],
                ])
                #print(row)
        setMessage(f"Archivo {option} leido correctamente")
        print(f"Archivo {option} leido correctamente")
        return data
    except Exception as e:  
        ErrorsNumber += 1      
        setMessage(str(e), 2)
        print(e)
    return None

def processPurchases(file1, file2): 
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = date.replace(' ', '_').replace(':', '_').replace('-', '_')
    outputFileName = f"retenciones_{date}.xlsx"       
    try:
        data1 = readFile(file1, 1)
        # sorting desc in the 9 index
        data1.sort(key=lambda x:x[9], reverse=True)
        data2 = readFile(file2, 2)
        for d1 in data1:
            for d2 in data2:
                if d1[0] == d2[0]:
                    d1[5] = d2[1]
                    d1[6] = d2[2]
                    #print(d2[2])
                    if d2[1] == '' or pd.isna(d2[1]) or d2[2] == '' or pd.isna(d2[2]):
                        print(f"Observación: el correlativo \"{d1[0]}\" no tiene número de control y/o sello de recepción")
                        setMessage(f"Observación: el correlativo \"{d1[0]}\" no tiene número de control y/o sello de recepción.", 2)
                    break
        setMessage("Registros filtrados y ordenados correctamente")
        df = pd.DataFrame(data1)
        df.to_excel(f"{os.path.dirname(file1)}/{outputFileName}", index=False, header=False)
        #print(data1[1])    
    except Exception as e:
        setMessage(str(e), 2)
        print(str(e))

#processPurchases("C:/Users/Desarrollador 2/Desktop/AMOR/NOTAS CREDITO ENERO2.xls", "C:/Users/Desarrollador 2/Desktop/AMOR/LIBRO DE COMPRAS.xlsx")
#print(getMessage())