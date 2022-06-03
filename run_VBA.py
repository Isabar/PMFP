# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:43:25 2022

@author: baret
"""
import win32com.client

def run_VBA():
    xl=win32com.client.Dispatch("Excel.Application")
    xl.Workbooks.Open(Filename=f'C:/Users/baret/Documents/Simulateur/Instances/macro1.xltm',ReadOnly=1)
    xl.Application.Run("Runnallmacro")
    xl.Workbooks(1).Close(SaveChanges=1)
    xl.Application.Quit()
    xl=0
    
    return 

run_VBA()