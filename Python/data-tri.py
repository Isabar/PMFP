# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 14:50:39 2022

@author: pcbaret
"""
import numpy as np
import pandas as pd
import csv 
import codecs
filename="C:/Users/baret/Documents/Resilience SC/data/Toronto/Distance2-euc.csv"

#test=np.genfromtxt(filename, dtype=[('mystring','S17')],delimiter=';', usecols=[0]).astype('str')
#data=np.loadtxt(filename,delimiter='\t',usecols=range(1,20))
#data=test[0].split(';')
"""for i in range (1,test.size()):
    data.append(test.split(';'))
"""""

def remove_char(path, name):
    f = codecs.open(path)
    contents = f.read()
    newcontents = contents.replace(',','.')
    g = open(name,"w+")
    g.write(newcontents)
    f.close()
    g.close()
    
def write_output(data):
    with open("C:/Users/baret/Documents/Resilience SC/data/Toronto/Distance-euc-restric.txt", "a") as fichier:
        for i in range(0,len(data)):
            fichier.write("{")
            for j in range(0,len(data[i])):
                fichier.write(str(data[i][j]))
                if (j != (len(data[i])-1)):
                    fichier.write(',')
            fichier.write('},\n')

def write_excel(data):
    with open("C:/Users/baret/Documents/Resilience SC/data/Toronto/Distance-tri.csv", "w") as fichier:
        writer=csv.writer(fichier)
        writer.writerows(data)

    
new="modif.csv"    

remove_char(filename, new)   
data=pd.read_csv(new, sep=';',encoding= 'unicode_escape')
nbdata=data.shape
dataTab=data.to_numpy()
si=dataTab.size
DataIndex=[]
for i in range(0,nbdata[0]):
    
    #print(dataTab[i])
    #for j in range(1,dataTab[i].size):
       # dataTab[i][j]=float(dataTab[i][j])
    Sort=sorted(dataTab[i][1:])
    indice=[]
    print("len sort: ",len(Sort))
    for j in range(0, len(Sort)):
        I=np.where(dataTab[i]==Sort[j])
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! I: ", I)
        print(Sort)
        print(type(I[0]))
        print(I[0])
        for k in range(0,len(I[0])):
            #if (dataTab[i][I[0][k]]<=0.03):
            indice.append(I[0][k])
            dataTab[i][I[0][k]]=-100
            print("data: ", dataTab)
            print("append :", I[0][k])
            print("indice : ", indice)
    DataIndex.append(indice)
    print(i)
write_excel(DataIndex)


"""
new="modif.csv"
# opening the CSV file 
remove_char(filename, new)

with open(filename, mode ='r')as file: 
      
  # reading the CSV file 
  csvFile = csv.reader(file) 
    
  # displaying the contents of the CSV file 
  for lines in csvFile: 
         data.append(lines)
         print("ligne",l
"""