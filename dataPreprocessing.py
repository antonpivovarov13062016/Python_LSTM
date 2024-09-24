import win32com.client
import os
import datetime
import numpy as np

#Считываем данные из таблиц

#Открытие файлов в корне приложения
xlApp = win32com.client.Dispatch("Excel.Application")
xlApp.Visible = True
workBookFromForm4EGS = xlApp.Workbooks.Open(f"{os.getcwd()}\\fromForm4EGS.xlsx")
workBookFromFormPM = xlApp.Workbooks.Open(f"{os.getcwd()}\\fromFormPM.xlsx")

#Списки для хранения значений таблиц
listsFromForm4EGS = []
listsFromFormPM = []

#Проходим каждый лист поотдельности, workBookFromForm4EGS
for n in range(1, workBookFromForm4EGS.Worksheets.Count+1):
    workSheetFromForm4EGS = workBookFromForm4EGS.Worksheets(n)
    workSheetFromForm4EGS.Activate()
    innerListFromForm4EGS = workSheetFromForm4EGS.Range("A2:BU17").Value
    listsFromForm4EGS.append(innerListFromForm4EGS)

#Проходим каждый лист поотдельности, listsFromFormPM
for n in range(1, workBookFromFormPM.Worksheets.Count+1):
    workSheetFromFormPM = workBookFromFormPM.Worksheets(n)
    workSheetFromFormPM.Activate()
    innerListFromFormPM = workSheetFromFormPM.Range("A3:BU18").Value
    listsFromFormPM.append(innerListFromFormPM)

workBookFromForm4EGS.Close()
workBookFromFormPM.Close()
xlApp.Quit()


print(listsFromForm4EGS)
#Проверка
print("listsFromForm4EGS, len=", len(listsFromForm4EGS))
print(listsFromForm4EGS[0])
print("listsFromFormPM, len=", len(listsFromFormPM))
print(listsFromFormPM[0])

#Преобразуем данные из листов Excel в массивы numpy
npFromForm4EGS = np.array(listsFromForm4EGS)
npFromFormPM = np.array(listsFromFormPM)

npTransposeFromForm4EGS = []
npTransposeFromFormPM = []

#Транспонируем таблицы, npFromForm4EGS  
for i in range(0, len(npFromForm4EGS)):
    npTransposeFromForm4EGS.append(npFromForm4EGS[i].transpose())

#Транспонируем таблицы, npFromFormPM  
for i in range(0, len(npFromFormPM)):
    npTransposeFromFormPM.append(npFromFormPM[i].transpose())

print("npTransposeFromForm4EGS[8]")
print(npTransposeFromForm4EGS[8])
print("npTransposeFromFormPM[13]")
print(npTransposeFromFormPM[13])



