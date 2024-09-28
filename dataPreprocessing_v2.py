import win32com.client
import os
import datetime
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import time

#https://habr.com/ru/articles/703246/
#в new_y лежит новый временный ряд без выбросов.
#в outliers - индексы выбросов во временном ряду.
#считаем, что данные подчиняются распределению Гаусса, поэтому берём коэффициент k равным 1,4826
def hampel(y, window_size, simg=3):    
    n = len(y)
    new_y = y.copy()
    k = 1.4826
    idx = []

    for i in range((window_size),(n - window_size)):
        r_median = np.median(y[(i - window_size):(i + window_size)]) #скользящая медиана 
        r_mad  = np.median(np.abs(y[(i - window_size):(i + window_size)] - r_median)) #скользящий MAD 
        if (np.abs(y.iloc[i].values[0] - r_median) > simg * r_mad):
            new_y.iat[i,0] = r_median #замена выброса
            idx.append(i)
    print("new_y")
    print(new_y.to_string())
    print("y")        
    print(y.to_string())
    return new_y, idx



#Начальные данные
nameFile1 = "fromForm4EGS.xlsx"
nameFile2 = "fromFormPM.xlsx"

dataFile1 = "A2:BU17"
dataFile2 = "A3:BU18"

dataNameFile1 = "A1"
dataNameFile2 = "A2"

#Считываем данные из таблиц

#Открытие файлов в корне приложения
xlApp = win32com.client.Dispatch("Excel.Application")
xlApp.Visible = True
workBookFromForm4EGS = xlApp.Workbooks.Open(f"{os.getcwd()}\\" + nameFile1)
workBookFromFormPM = xlApp.Workbooks.Open(f"{os.getcwd()}\\" + nameFile2)

#Списки для хранения значений таблиц
listsFromForm4EGS = []
listsFromFormPM = []

#Названия таблиц
listNameTableFromForm4EGS = []
listNameTableFromFormPM = []

#Списки DataFrame
dictionaryDataFrameFromForm4EGS = []
dictionaryDataFrameFromFormPM = []

#Проходим каждый лист поотдельности, workBookFromForm4EGS
for n in range(1, workBookFromForm4EGS.Worksheets.Count+1):
    workSheetFromForm4EGS = workBookFromForm4EGS.Worksheets(n)
    workSheetFromForm4EGS.Activate()
    innerListFromForm4EGS = workSheetFromForm4EGS.Range(dataFile1).Value
    listsFromForm4EGS.append(innerListFromForm4EGS)
    listNameTableFromForm4EGS.append(workSheetFromForm4EGS.Range(dataNameFile1).Value)

#Проходим каждый лист поотдельности, listsFromFormPM
for n in range(1, workBookFromFormPM.Worksheets.Count+1):
    workSheetFromFormPM = workBookFromFormPM.Worksheets(n)
    workSheetFromFormPM.Activate()
    innerListFromFormPM = workSheetFromFormPM.Range(dataFile2).Value
    listsFromFormPM.append(innerListFromFormPM)
    listNameTableFromFormPM.append(workSheetFromFormPM.Range(dataNameFile2).Value)

workBookFromForm4EGS.Close()
workBookFromFormPM.Close()
xlApp.Quit()


#Проверка
print("listsFromForm4EGS, len=", len(listsFromForm4EGS))
print(listsFromForm4EGS[0])
print("listsFromFormPM, len=", len(listsFromFormPM))
print(listsFromFormPM[0])

print("NamesList")
print(listNameTableFromForm4EGS)
print(listNameTableFromFormPM)

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

print("npTransposeFromForm4EGS[0]")
print(npTransposeFromForm4EGS[0])
print("npTransposeFromFormPM[0]")
print(npTransposeFromFormPM[0])

#Сохраняем преобразованние данные в npy формат
for i in range(0, len(npTransposeFromForm4EGS)):
    np.save("npy\\FromForm4EGS_" + str(i), npTransposeFromForm4EGS[i])

for i in range(0, len(npTransposeFromFormPM)):
    np.save("npy\\FromFormPM_" + str(i), npTransposeFromFormPM[i])

#Преобразовать массив numpy в dataframe pandas
for npTable in npTransposeFromForm4EGS:
    dictionaryDataFrameFromForm4EGS.append(   pd.DataFrame(data=npTable[1:,:], index=np.array(range(1, len(npTable))), columns=npTable[0,:])  )

for npTable in npTransposeFromFormPM:
    dictionaryDataFrameFromFormPM.append(   pd.DataFrame(data=npTable[1:,:], index=np.array(range(1, len(npTable))), columns=npTable[0,:])  )

for i in range(0, len(dictionaryDataFrameFromForm4EGS)):
    dictionaryDataFrameFromForm4EGS[i] = dictionaryDataFrameFromForm4EGS[i].apply(pd.to_numeric)

for i in range(0, len(dictionaryDataFrameFromFormPM)):
    dictionaryDataFrameFromFormPM[i] = dictionaryDataFrameFromFormPM[i].apply(pd.to_numeric)


dictionaryDataFrameFromForm4EGS[0].info()
dictionaryDataFrameFromFormPM[0].info()

dictionaryDataFrameFromForm4EGS[0].describe()
dictionaryDataFrameFromFormPM[0].describe()

print(listNameTableFromForm4EGS[0]+"\\" + dictionaryDataFrameFromForm4EGS[0].columns[2:2+1].values + ".jpg")
lenColumns = len(list(dictionaryDataFrameFromForm4EGS[0].columns[:].values))
print(lenColumns)

if not os.path.exists("fromFormPM"):
            os.mkdir("fromFormPM")
if not os.path.exists("fromForm4EGS"):
            os.mkdir("fromForm4EGS")

#test
dfTest = dictionaryDataFrameFromFormPM[0][dictionaryDataFrameFromFormPM[0].columns[2:3].values]
            
new_y, outliers = hampel(dfTest, 6)
df = new_y
print(df)
print(outliers)
plt.figure(figsize=(15, 6), dpi=80)
plt.plot(df)
plt.savefig("end.jpg")
plt.close()
#plot
plt.plot(dfTest)
plt.savefig("begin.jpg")
plt.close()




#Вывод и сохранение графиков
for i in range(0, len(listNameTableFromForm4EGS)):
    
#correlation
    df = dictionaryDataFrameFromForm4EGS[i][dictionaryDataFrameFromForm4EGS[i].columns[2:].values]
    # Plot
    plt.figure(figsize=(24,20), dpi= 80)
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
    # Decorations
    plt.title('Correlogram of regions', fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    if not os.path.exists(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i])):
            os.makedirs(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i]))
    plt.savefig("fromForm4EGS\\CorrelogramOfRegions_"+listNameTableFromForm4EGS[i] + ".jpg")
    plt.close()
    
    for j in range(2, lenColumns):
        if not os.path.exists(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'hist')):
            os.makedirs(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'hist'))
        if not os.path.exists(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'plot')):    
            os.makedirs(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'plot'))
        if not os.path.exists(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'boxplot')):    
            os.makedirs(os.path.join('fromForm4EGS', listNameTableFromForm4EGS[i], 'boxplot'))
        title = str(dictionaryDataFrameFromForm4EGS[i].columns[j:j+1].values).replace(".","").replace("'","").replace("[","").replace("]","").replace('\\\\',"").replace('\\',"").replace("/","")
        
#plot
        plt.title(title)
        plt.plot(dictionaryDataFrameFromForm4EGS[i][dictionaryDataFrameFromForm4EGS[i].columns[j:j+1].values])
        plt.savefig("fromForm4EGS\\"+listNameTableFromForm4EGS[i] + "\\plot\\" + title + ".jpg")
        plt.close()
#hist
        plt.title(title)
        plt.hist(dictionaryDataFrameFromForm4EGS[i][dictionaryDataFrameFromForm4EGS[i].columns[j:j+1].values])
        plt.savefig("fromForm4EGS\\"+listNameTableFromForm4EGS[i] + "\\hist\\" + title + ".jpg")
        plt.close()
#boxplot
        plt.title(title)
        plt.boxplot(dictionaryDataFrameFromForm4EGS[i][dictionaryDataFrameFromForm4EGS[i].columns[j:j+1].values], patch_artist=True, vert=0)
        plt.savefig("fromForm4EGS\\"+listNameTableFromForm4EGS[i] + "\\boxplot\\" + title + ".jpg")
        plt.close()

        

    
for i in range(0, len(listNameTableFromFormPM)):

#correlation
    df = dictionaryDataFrameFromFormPM[i][dictionaryDataFrameFromFormPM[i].columns[2:].values]
    # Plot
    plt.figure(figsize=(24,20), dpi= 80)
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
    # Decorations
    plt.title('Correlogram of regions', fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    if not os.path.exists(os.path.join('fromFormPM', listNameTableFromFormPM[i])):
            os.makedirs(os.path.join('fromFormPM', listNameTableFromFormPM[i]))
    plt.savefig("fromFormPM\\CorrelogramOfRegions_"+listNameTableFromFormPM[i] + ".jpg")
    plt.close()
    
    for j in range(2, lenColumns):
        if not os.path.exists(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'hist')):
            os.makedirs(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'hist'))
        if not os.path.exists(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'plot')):    
            os.makedirs(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'plot'))
        if not os.path.exists(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'boxplot')):    
            os.makedirs(os.path.join('fromFormPM', listNameTableFromFormPM[i], 'boxplot'))
        title = str(dictionaryDataFrameFromFormPM[i].columns[j:j+1].values).replace(".","").replace("'","").replace("[","").replace("]","").replace('\\\\',"").replace('\\',"").replace("/","")
        
#plot
        plt.title(title)
        plt.plot(dictionaryDataFrameFromFormPM[i][dictionaryDataFrameFromFormPM[i].columns[j:j+1].values])
        plt.savefig("fromFormPM\\"+listNameTableFromFormPM[i] + "\\plot\\" + title + ".jpg")
        plt.close()
#hist
        plt.title(title)
        plt.hist(dictionaryDataFrameFromFormPM[i][dictionaryDataFrameFromFormPM[i].columns[j:j+1].values])
        plt.savefig("fromFormPM\\"+listNameTableFromFormPM[i] + "\\hist\\" + title + ".jpg")
        plt.close()
#boxplot
        plt.title(title)
        plt.boxplot(dictionaryDataFrameFromFormPM[i][dictionaryDataFrameFromFormPM[i].columns[j:j+1].values], patch_artist=True, vert=0)
        plt.savefig("fromFormPM\\"+listNameTableFromFormPM[i] + "\\boxplot\\" + title + ".jpg")
        plt.close()
        
#Поиск выбросов и их замена
        new_y, outliers = hampel(dictionaryDataFrameFromFormPM[0][dictionaryDataFrameFromFormPM[i].columns[2:3].values], 3)
        df = new_y
        df.loc[outliers, 'outlier_hampel'] = 1
        plt.figure(figsize=(15, 6), dpi=80)
        plt.plot(df)
        plt.show()
#Вывод результата
        
#Нормализация

