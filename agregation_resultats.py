# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:14:43 2022

@author: baret
"""

import pandas as pd
import xlsxwriter
import numpy as np

def aggr_result(directory, instance_size,model):
    file_result='C:/Users/baret/Documents/Simulateur/Resultats.xlsx'
    workbook = xlsxwriter.Workbook(file_result)
    worksheet = workbook.add_worksheet('Result')
    worksheet.write('A1','Instance')
    worksheet.write('B1','nbClients')
    worksheet.write('C1','nbFacilities')
    worksheet.write('D1','Coefficient de congestion')
    worksheet.write('E1','Resolution Time')
    
    for i in range(instance_size) :
        fichier= (directory + f'/Instances/Instance{i}.xlsx')
        fichierSol= (directory + f'/Resultats/instance_{i}_{model}_False.xlsx')
        #donnees générales 
            
        Donnees=pd.read_excel(fichier,sheet_name="Donnees", index_col=0 )
        Congestion=pd.read_excel(fichier,sheet_name="Congestions", index_col=0 )       
        #données facilities 
 #       Capacites=pd.read_excel(fichier,sheet_name="Congestions", index_col=0 )
                
        Do=Donnees.to_numpy()
        C=Congestion.to_numpy()
               
         # données solutions   
        Resolution_time=pd.read_excel(fichierSol,sheet_name="Sheet1", index_col=0)
        RT=Resolution_time.to_numpy()

        R=RT.size
        if R>0:
            ResT=RT[0,3]
            worksheet.write(i+1,4,ResT)
        nbClients=Do[0]
        nbFacilities=Do[1]
        worksheet.write(i+1,0,i)
        worksheet.write(i+1,1,nbClients)
        worksheet.write(i+1,2,nbFacilities)
        
        print(C.size)
      #  C2=np.resize(C,(1,nbClients))
        ET=np.std(C)
        print(ET)
        M=np.mean(C)
        print(M)
        CO=ET/M
        worksheet.write(i+1,3,CO)
        #worksheet.write(i+1,3,ResT)
        print(ResT)
    workbook.close()
    return 
        


def compare_result(directory,instance_size):
    file_result='C:/Users/baret/Documents/Simulateur/Resultats-compare.xlsx'
    workbook = xlsxwriter.Workbook(file_result)
    worksheet = workbook.add_worksheet('Result')
    
    worksheet.write('A1','Instance')
    worksheet.write('B1','nbClients')
    worksheet.write('C1','nbFacilities')
    worksheet.write('D1','Coefficient de congestion')
    worksheet.write('E1','Resolution Time Non relaxé')
    worksheet.write('F1','Resolution Time Relaxé')
    worksheet.write('G1',' Nb Var Diff')
    worksheet.write('H1','Diff Obj')
    
    for i in range(instance_size) :
        fichier= (directory + f'/Instances/Instance{i}.xlsx')
        fichierSolNR= (directory + f'/Resultats/instance_{i}_False.xlsx')
        fichierSolR= (directory + f'/Resultats/instance_{i}_True.xlsx')
        #donnees générales 
            
        Donnees=pd.read_excel(fichier,sheet_name="Donnees", index_col=0 )
        Congestion=pd.read_excel(fichier,sheet_name="Congestions", index_col=0 )       
        #données facilities 
 #       Capacites=pd.read_excel(fichier,sheet_name="Congestions", index_col=0 )
                
        Do=Donnees.to_numpy()
        C=Congestion.to_numpy()
         
        nbClients=Do[0]
        nbFacilities=Do[1]
        worksheet.write(i+1,0,i)
        worksheet.write(i+1,1,nbClients)
        worksheet.write(i+1,2,nbFacilities)
        
         # données solutions   
        Resolution_timeNR=pd.read_excel(fichierSolNR,sheet_name="Sheet1", index_col=0)
        RTNR=Resolution_timeNR.to_numpy()

        R=RTNR.size
        if R>0:
            ResT=RTNR[0,3]
            worksheet.write(i+1,4,ResT)
            ResNR=RTNR[1:,0]
            print(ResNR)
        else :
            ResNR=np.empty(shape=1)
        Resolution_timeR=pd.read_excel(fichierSolR,sheet_name="Sheet1", index_col=0)
        RTR=Resolution_timeR.to_numpy()

        RR=RTR.size
        if RR>0:
            ResT=RTR[0,3]
            worksheet.write(i+1,5,ResT)
            ResR=RTR[1:,0]
            print(ResR)
        else :
            ResR=np.empty(shape=1)
        nbVArDiff=0
        print(ResR.size)
        print(ResNR.size)
       
        for j in range(min(ResNR.size,ResR.size)):
            if ResNR[j] != ResR[j]:
                nbVArDiff=nbVArDiff+1
        
        DiffScore=0
        if R>0 & RR>0:
            DiffScore=RTR[0,1]-RTNR[0,1]
            
      #  C2=np.resize(C,(1,nbClients))
        ET=np.std(C)

        M=np.mean(C)

        CO=ET/M
        worksheet.write(i+1,3,CO)
        worksheet.write(i+1,6,nbVArDiff)
        worksheet.write(i+1,7,DiffScore)
    workbook.close()
    
    
    
directory='C:/Users/baret/Documents/Simulateur/'     
model='C'  
RT=aggr_result(directory, 10,model)
#compare_result(directory, 30)