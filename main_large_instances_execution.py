import  os
from lingo_relation import *
from Generator import *
#from agregation_resultats import *
#from interface_animation import *
import xlsxwriter



def crea_instance(instance_size,minClients,maxClients,minDemand,maxDemand,penality,minFacilities,maxFacilities, nbLevels, cost, probaInit):

    for i in range(instance_size):
        nbClients,nbFacilities,Distances,Penalities,Demand,Budget,Ki,Positions,Capacites,ProbaL,ProbaCO, ProbaCOCA,Cost, positionC, positionF, congestion=Generator(minClients,maxClients,minDemand,maxDemand,penality,minFacilities,maxFacilities, nbLevels, cost, probaInit)
        filename='C:/Users/baret/Documents/Simulateur/Instances/Instance'+str(i)+'.xlsx'
        re=excel_write(filename, nbClients,nbFacilities,Budget,Demand,Penalities,Distances,Cost,ProbaL,ProbaCO, ProbaCOCA,Ki,Positions,nbLevels, congestion, Capacites, positionC, positionF);
        #display_instance(filename)
    return 

 

def resolution(instance_debut,instance_fin, directory, model,relaxed,cap,typeProba):
    #3
    instances = [(i) for i in range(instance_debut,instance_fin)]

    for instance in instances:
        create_lingo_ltf_file(directory,instance,model,relaxed,cap,typeProba)
        print('running instance '+str(instance) )
        fileSol= directory+'/Resultats/instance_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.xlsx'
       # print(fileSol)
        workbook = xlsxwriter.Workbook(fileSol)

        workbook.close()
        filemodel=directory+'/Modeles/model_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.ltf'
       # print(filemodel)
        os.system(f'runlingo {filemodel}')

    return 

   
instance_size=30
#crea_instance(instance_size, 50, 240, 10, 12, 10, 5, 24, 4, 10, 0.3)
print('test')
relaxed =False
model='C' # C ou CMS ou CML 
cap=4
directory='C:/Users/baret/Documents/Simulateur/Instances-finales/Instances-24-240-0,1'
resolution(7,8,directory,model,False, cap,'Linear')
#resolution(instance_size,model,True, cap,'Linear')
model2='Normal'
#resolution(0,30, model2, False,cap,'Linear')

