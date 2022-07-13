# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 15:44:37 2022

@author: baret
"""

from lingo_bi_obj import *
import xlsxwriter
import os

def resolution_bi_obj(instance_debut,instance_fin, directory, model,relaxed,cap,typeProba):
    #3
    instances = [(i) for i in range(instance_debut,instance_fin)]

    for instance in instances:
        create_lingo_bi_obj(directory,instance,model,relaxed,cap,typeProba)
        print('running instance '+str(instance) )
        fileSol= directory+'/Resultats/instance_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.xlsx'
       # print(fileSol)
        workbook = xlsxwriter.Workbook(fileSol)

        workbook.close()
        filemodel=directory+'/Modeles/model_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.ltf'
        print(filemodel)
        os.system(f'runlingo {filemodel}')

    return 

directory='C:/Users/baret/Documents/Simulateur/test-normalisation/Tests-max/Instances-12-120-0,3/NR/Cap4'
relaxed =False
model='C' # C ou CMS ou CML 
cap=4

resolution_bi_obj(7,30, directory, model, relaxed, cap, 'Linear')