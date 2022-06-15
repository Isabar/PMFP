# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 14:12:00 2022

@author: baret
"""
from agregation_resultats import *
import numpy as np
import pandas as pd
#from interface_animation import *
import xlsxwriter


def analyse(i,directory):
    
    filename=directory+'/Instances/Instance'+str(i)+'.xlsx'
    
    fileSol=directory+'/Resultats/instance_'+str(i)+'_C_False.xlsx'
   
    fileAnalyse = directory+'/Analyse/Analyse'+str(i)+'.xlsx'
    workAnalyse=xlsxwriter.Workbook(fileAnalyse)
    worksheet = workAnalyse.add_worksheet('Result')
    worksheet.write('A1','Etablissements')
    worksheet.write('B1','Congestion')
    worksheet.write('C1','Distance')
    worksheet.write('D1','Capacité')
    worksheet.write('E1','Distance clients 1')
    worksheet.write('F1','Distance établissements')
    worksheet.write('G1','Niveau de fortication')
    
    Do= pd.read_excel(filename,sheet_name="Donnees", index_col=0 )
    Donnees=Do.to_numpy()
    nbClients=Donnees[0]
    nbFacilities=Donnees[1]
    nbLevels=Donnees[3]
    Cong=pd.read_excel(filename, sheet_name='Congestions', index_col=0)
    Congestions=Cong.to_numpy()
    PC=pd.read_excel(filename, sheet_name='Position-client', index_col=0)
    PositionsC=PC.to_numpy()
    PF=pd.read_excel(filename, sheet_name='Position-facilities', index_col=0)
    PositionsF=PF.to_numpy()
    Cap=pd.read_excel(filename,sheet_name='Capacites', index_col=0)
    Capacites=Cap.to_numpy()
    T = pd.read_excel(filename,sheet_name='Tri', index_col=0)
    Tri=T.to_numpy()
    nbC=int(nbClients)
    nbF=int(nbFacilities)
    nbL=int(nbLevels)
    DistC1=calc_dist_Client1(nbC,nbF, Tri, PositionsC,PositionsF)
    DistF=cal_dist(nbF, nbF, PositionsF, PositionsF)
    Sol=get_sol(nbFacilities,fileSol)

    Dist=cal_dist(nbC,nbF,PositionsC,PositionsF)
    
    for k in range (nbF):
        ligne=k+1
        worksheet.write(ligne,0,k)
        worksheet.write(ligne,1,Congestions[k])
        worksheet.write(ligne,2, Dist[k])
        worksheet.write(ligne,3, Capacites[k])
        #print('Dist')
        #print(k)
        #print(DistC1)
        worksheet.write(ligne,4, DistC1[k])
        worksheet.write(ligne,5, DistF[k])
        for l in range(nbL):
            if Sol[k,l]==1:
                worksheet.write(ligne,6,l)
    workAnalyse.close()
    return 


def cal_dist(nbC,nbF, PC,PF):

    D=np.zeros((nbC, nbF))
    for i in range(nbC):
        for k in range(nbF):
            D[i,k]=abs(PC[i,0]-PF[k,0])**2+abs(PC[i,1]-PF[k,1])**2
    dist=np.zeros(nbF)

    for kk in range(nbF):
        dist[kk]=np.sum(D[:,kk])/(nbC)
  #  print(dist)
    return dist
    
def calc_dist_Client1(nbClients,nbFacilities, Tri, PC,PF ):
    D=np.zeros((nbClients, nbFacilities))
    nbC1=np.zeros(nbFacilities)
    for i in range (nbClients):
        for k in range(nbFacilities):
           # print(Tri)
           if Tri[i,0]==(k+1):
                D[i,k]=abs(PC[i,0]-PF[k,0])**2+abs(PC[i,1]-PF[k,1])**2
                nbC1[k]=nbC1[k]+1
    dist=np.zeros(nbFacilities)
   # print(D)
   # print(D.size)
    print(nbC1)
    for kk in range(nbFacilities):
        if nbC1[kk]>0:
            dist[kk]=(np.sum(D[:,kk]))/(nbC1[kk])
        else :
            dist[kk]=0
  #  print(dist)
    return dist


directory='C:/Users/baret/Documents/Simulateur/Instances-finales/Instances-12-120-0,1/NR/Convex'
instance_size=30
for i in range(instance_size):
    analyse(i,directory)
    