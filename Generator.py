# -*- coding: utf-8 -*-
"""
Created on Wed May 11 16:36:27 2022

@author: baret
"""
import random
import numpy as np

import xlsxwriter
import copy
from xlsxwriter.utility import xl_range

def Generator(minClients,maxClients,minDemand,maxDemand,penality,minFacilities,maxFacilities, nbLevels, cost, probaInit, typeProba):
    nbClients= random.randint(minClients,maxClients)
    Demand=np.zeros(nbClients)
    Penalities=np.zeros(nbClients)
    positionC=np.zeros((nbClients,2))
    for i in range(nbClients) :
        Demand[i]= random.randint(minDemand,maxDemand)
        Penalities[i]=penality
        positionC[i,0]=10*random.random()
        positionC[i,1]=10*random.random()

    # donnees etablissements
    nbFacilities= random.randint(minFacilities,maxFacilities)
    positionF=np.zeros((nbFacilities,2))
    for k in range(nbFacilities) :
       positionF[k,0]=10*random.random()
       positionF[k,1]=10*random.random()
       
    # calcul de distances
    Distances=calc_distance(nbClients, nbFacilities, positionC, positionF)
    
    # calcul des probabilites 
    Cost,Proba=calc_proba(nbClients, nbFacilities, nbLevels, cost, probaInit, typeProba)
    Budget=nbFacilities*(nbLevels-1)*10

    # calcul des Ki
    Ki=calc_tri(nbClients, nbFacilities, Distances)

    #calcul des positions 
    Positions=calc_positions(nbClients, nbFacilities, Ki)
    
    #calcul capacites et congestion 
    Capacites,Congestion=Calc_Congestion(nbClients,nbFacilities,Demand,Positions)
    
    return nbClients,nbFacilities,Distances,Penalities,Demand,Budget,Ki,Positions,Capacites,Proba,Cost, positionC, positionF, Congestion 


def excel_write(filename, nbClients,nbFacilities,Budget,demand,penalites,distances,cost,proba,Ki,positions,nbLevels, congestion, capacites, positionC,positionF):
   
    workbook = xlsxwriter.Workbook(filename)
    worksheetD = workbook.add_worksheet('Donnees')
    worksheetD.write('A2', 'nbClients')
    worksheetD.write('A3', 'nbFacilities')
    worksheetD.write('A4', 'Budget')
    worksheetD.write('A5', 'nbLevels')
    worksheetD.write('B2', nbClients)
    worksheetD.write('B3', nbFacilities)

    B=0.3*Budget

    worksheetD.write('B4', B)
    worksheetD.write('B5', nbLevels)
    
    workbook.define_name('NbClients', '=Donnees!$B$2')
    workbook.define_name('NbFacilities', '=Donnees!$B$3')
    workbook.define_name('Budget', '=Donnees!$B$4')
    workbook.define_name('NbLevels', '=Donnees!$B$5')
    
    worksheetC = workbook.add_worksheet('Clients')
    worksheetC.write_string(0,1,'Demandes')
    for i in range(nbClients):
       worksheetC.write(i+1,1,demand[i])
    worksheetC.write_string(0,2,'Penalites')
    for i in range(nbClients):
        worksheetC.write(i+1,2,penalites[i])
    workbook.define_name('Demandes',  f'=Clients!$B$2:$B${nbClients+1}')
    workbook.define_name('Penalites',  f'=Clients!$C$2:$C${nbClients+1}')
  
    worksheetDi = workbook.add_worksheet('Distances')
    for i in range(nbClients):
        for k in range(nbFacilities):
            worksheetDi.write(i+1,k+1,distances[i,k])
    cell_range_dist=xl_range(1,1,nbClients+1,nbFacilities+1)     
    workbook.define_name('Distances', f'=Distances!{cell_range_dist}')
    
    worksheetCo = workbook.add_worksheet('Proba')
    for k in range(nbFacilities):
        for l in range(nbLevels):
            worksheetCo.write(k+1,l+1,cost[k,l])
    
    for k in range(nbFacilities):
        for l in range(nbLevels):
            worksheetCo.write(k+1,(2*nbLevels)+l,proba[k,l])
    cell_range_cost=xl_range(1,1,nbFacilities+1,nbLevels+1)
    cell_range_proba=xl_range(1,8,nbFacilities+1,7+nbLevels+1)

    workbook.define_name('Cout', f'=Proba!{cell_range_cost}')
    workbook.define_name('Proba', f'=Proba!{cell_range_proba}')
     
    worksheetT = workbook.add_worksheet('Tri')
    for i in range(nbClients):
        for k in range(nbFacilities):
            worksheetT.write(i+1,k+1,Ki[i,k])     
    cell_range_tri=xl_range(1,1,nbClients+1,nbFacilities+1)     
    workbook.define_name('Tri', f'=Tri!{cell_range_tri}')
    
    worksheetP = workbook.add_worksheet('Positions')
    for i in range(nbClients):
        for k in range(nbFacilities):
            worksheetP.write(i+1,k+1,positions[i,k])     
    cell_range_pos=xl_range(1,1,nbClients+1,nbFacilities+1)     
    workbook.define_name('Positions', f'=Positions!{cell_range_pos}')
    
    worksheetCon = workbook.add_worksheet('Congestions')
    for k in range(nbFacilities):
        worksheetCon.write(k+1,1,congestion[k])       
    workbook.define_name('Congestions', f'=Congestions!$B$2:B{nbFacilities+1}')
    
    worksheetCap = workbook.add_worksheet('Capacites')
    for k in range(nbFacilities):
        worksheetCap.write(k+1,1,capacites[k])      
    workbook.define_name('Capacites', f'=Capacites!$B$2:B{nbFacilities+1}')
    
    worksheetPoC = workbook.add_worksheet('Position-client')
    for i in range(nbClients):
        for l in range(2):
            worksheetPoC.write(i+1,l+1,positionC[i,l])
            
    worksheetPoF = workbook.add_worksheet('Position-facilities')
    for k in range(nbFacilities):
        for l in range(2):
             worksheetPoF.write(k+1,l+1,positionF[k,l])
    
    workbook.close()

   
    return 

def calc_distance(nbClients, nbFacilities, positionC, positionF ):
    Distances= np.zeros((nbClients, nbFacilities))
    for i in range(nbClients) :
        for j in range(nbFacilities) :
            Distances[i,j]=abs(positionC[i,0]-positionF[j,0])**2+abs(positionC[i,1]-positionF[j,1])**2
    return Distances
    
def calc_tri(nbClients, nbFacilities, Distances):
    Ki=np.zeros((nbClients,nbFacilities))
    distances2=copy.deepcopy(Distances)
    for i  in range(nbClients) :
        Min=min(distances2[i][0:])
        for j in range(nbFacilities):
            Min=min(distances2[i][0:])
            I=np.where(distances2[i]==Min)

            Ki[i,j]=I[0][0]+1
            distances2[i][I[0][0]]=1000
    return Ki 

def calc_positions(nbClients, nbFacilities,Ki):
    Positions=np.zeros((nbClients,nbFacilities))
    for i in range(nbClients):
        for k in range(1,nbFacilities+1):
            lst = np.array(Ki[i])
            I=np.where(lst==k)
          
            Positions[i,k-1]=(int(I[0][0])+1)
    return Positions
    
def calc_proba(nbClient, nbFacilities,nbLevels, cost,probaInit,typeProba):
    Proba=np.zeros((nbFacilities, nbLevels))
    Cost=np.zeros((nbFacilities, nbLevels))
    for k in range(nbFacilities) :
        for l in range(nbLevels ): 
            Cost[k,l]=(l)*cost
            print(l)
            if l==0 :
                Proba[k,l]=probaInit-((probaInit-(0.5*probaInit)/2**l)/nbLevels)*l
                print(Proba[k,l])
            elif l>=1 :
                if typeProba=='Linear':
                    Proba[k,l]=probaInit-((probaInit-(0.5*probaInit)/2**l)/nbLevels)*l
                    print(Proba[k,l])
                elif typeProba=='Convex':
                    Proba[k,l]=probaInit/(2**l)
                elif  typeProba=='Concave':
                    Proba[k,l]= probaInit*(((nbLevels-l)/nbLevels)**0.6)
    print(Proba)
    return Cost, Proba
    
def Calc_Congestion(nbClients,nbFacilities,Demand,Positions):
    
    Congestion=np.zeros(nbFacilities)
    Cap_init=np.zeros(nbFacilities)
    for k in range(nbFacilities):
        C=0
        Ca=0
        for i in range(nbClients):
            C=C+Demand[i]*(nbFacilities-Positions[i,k])
            if Positions[i,k]==1:
                Ca=Ca+Demand[i]
        Congestion[k]=C
        Cap_init[k]=Ca

    return Congestion, Cap_init