# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 10:32:02 2022

@author: baret
"""

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


def aggr_result(directory, instance_size,model):
    file_result=directory + '/Resultats.xlsx'
    workbook = xlsxwriter.Workbook(file_result)
    worksheet = workbook.add_worksheet('Result')
    worksheet.write('A1','Instance')
    worksheet.write('B1','nbClients')
    worksheet.write('C1','nbFacilities')
    worksheet.write('D1','Coefficient de congestion')
    worksheet.write('E1','Resolution Time')
    worksheet.write('F1','Niveau 0')
    worksheet.write('G1','Niveau 1')
    worksheet.write('H1','Niveau 2')
    worksheet.write('I1','Niveau 3')
    worksheet.write('J1','Distance Facilities')
    worksheet.write('K1','Distance Clients')
    worksheet.write('L1','Ecart bi obj')
    
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
        
        
      #  C2=np.resize(C,(1,nbClients))
        ET=np.std(C)

        M=np.mean(C)
        CO=ET/M
        worksheet.write(i+1,3,CO)
        
        NS=get_sol(nbFacilities, fichierSol)
        N0=0
        N1=0
        N2=0
        N3=0
        NbF=int(nbFacilities)
        for k in range(NbF):
            if NS[k,0]==1:
                N0=N0+1
            elif NS[k,1]==1:
                N1=N1+1
            elif NS[k,2]==1:
                N2=N2+1
            elif NS[k,3]==1:
                N3=N3+1

        worksheet.write(i+1,5,N0)
        worksheet.write(i+1,6,N1)
        worksheet.write(i+1,7,N2)
        worksheet.write(i+1,8,N3)
    
        PositionsFacilities=pd.read_excel(fichier,sheet_name="Position-facilities", index_col=0 )
        
        positionF=PositionsFacilities.to_numpy()
        PF=positionF.size
        if PF>0 :
            D=calcul_distance(NbF, positionF)
            worksheet.write(i+1,9,D)
        
        PositionsClients=pd.read_excel(fichier,sheet_name="Position-client", index_col=0 )
        positionC=PositionsClients.to_numpy()
        PC=positionC.size
        if PC>0 :
            D=calcul_distance(NbF, positionC)
            worksheet.write(i+1,10,D)
        H1,H2=get_bi_obj(fichierSol)
        if H2>0:
            worksheet.write(i+1,11,H1/H2)
        else :
           worksheet.write(i+1,11,0) 
    workbook.close()
    return 
        



def get_bi_obj(filename):
    Solutions=pd.read_excel(filename,sheet_name="Sheet1", index_col=0)
    S=Solutions.to_numpy()
    print(S)
    if S.size>0: 
        H1=S[2,2]
        H2=S[2,3]
        print(H1,H2)
    else :
        H1=0
        H2=0
    return H1,H2


#directory='C:/Users/baret/Documents/Simulateur/Test-capacité/120-12'    
#directory='C:/Users/baret/Documents/Simulateur/Test-capacité'
directory='C:/Users/baret/Documents/Simulateur/test-normalisation/Tests-max/Instances-12-120-0,3/NR/Cap4'
aggr_result(directory, 30, 'C')