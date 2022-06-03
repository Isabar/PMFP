import  os
from lingo_relation import *
from Generator import *
#from agregation_resultats import *
from interface_animation import *



def crea_instance(instance_size,minClients,maxClients,minDemand,maxDemand,penality,minFacilities,maxFacilities, nbLevels, cost, probaInit, typeProba):

    for i in range(instance_size):
        nbClients,nbFacilities,Distances,Penalities,Demand,Budget,Ki,Positions,Capacites,Proba,Cost, positionC, positionF, congestion=Generator(minClients,maxClients,minDemand,maxDemand,penality,minFacilities,maxFacilities, nbLevels, cost, probaInit, typeProba)
        filename='C:/Users/baret/Documents/Simulateur/Instances/Instance'+str(i)+'.xlsx'
        re=excel_write(filename, nbClients,nbFacilities,Budget,Demand,Penalities,Distances,Cost,Proba,Ki,Positions,nbLevels, congestion, Capacites, positionC, positionF);
        #display_instance(filename)
    return 

 

def resolution(instance_size,model,relaxed,cap):
    #3
    instances = [(i) for i in range(instance_size)]

    for instance in instances:
        create_lingo_ltf_file(instance,model,relaxed,cap)
        print('running instance '+str(instance) )
        fileSol= 'C:/Users/baret/Documents/Simulateur/Resultats/instance_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.xlsx'
        workbook = xlsxwriter.Workbook(fileSol)
        os.system(f'runlingo C:/Users/baret/Documents/Simulateur/Modeles/model_{instance}_{model}_{relaxed}.ltf')
    workbook.close()
    return 

"""
def analyse_result(instance_size):
    directory='C:/Users/baret/Documents/Simulateur/'       
    RT=aggr_result(directory, 30)
    compare_result(directory, 30)

 """   
instance_size=10
crea_instance(instance_size, 50, 240, 10, 30, 10, 5, 12, 4, 10, 0.3, 'Linear')
print('test')
relaxed =False
model='C' # C ou CMS ou CML 
cap=2
resolution(instance_size,model,False, cap)
#resolution(instance_size,model,True)
#model2='Normal'
#resolution(instance_size, model2, False,cap)

