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

 

def resolution(instance_size,model,relaxed,cap,typeProba):
    #3
    instances = [(i) for i in range(instance_size)]

    for instance in instances:
        create_lingo_ltf_file(instance,model,relaxed,cap,typeProba)
        print('running instance '+str(instance) )
        fileSol= 'C:/Users/baret/Documents/Simulateur/Resultats/instance_'+str(instance)+'_'+str(model)+'_'+str(relaxed)+'.xlsx'
        print(fileSol)
        workbook = xlsxwriter.Workbook(fileSol)

        workbook.close()
        os.system(f'runlingo C:/Users/baret/Documents/Simulateur/Modeles/model_{instance}_{model}_{relaxed}.ltf')

    return 

"""
def analyse_result(instance_size):
    directory='C:/Users/baret/Documents/Simulateur/'       
    RT=aggr_result(directory, 30)
    compare_result(directory, 30)

 """   
instance_size=30
#crea_instance(instance_size, 50, 120, 10, 12, 10, 5, 12, 4, 10, 0.1)
print('test')
relaxed =False
model='C' # C ou CMS ou CML 
cap=4
resolution(instance_size,model,False, cap,'Linear')
#resolution(instance_size,model,True, cap,'Linear')
model2='Normal'
#resolution(instance_size, model2, False,cap,'Linear')

