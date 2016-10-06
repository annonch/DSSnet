#####################
#    event handling #
#####################
#  channon@iit.edu  #
#####################
#      DSSnet       #
#    Version 2.0    #
#####################

#this file holds preprocessing events for custom synchronization requests 

#   The function name must match line[3]

#Input parameters are engine, args circuit and event as a string
import dss

def controllable_load(circuit,engine,args,line):
	result = dss.updateL(engine,line[6],line[5],args.et,line[8])
	return result

def controllable_generator(circuit,engine,args,line):
	result = dss.updateG(engine,line[6],line[5],args.et,line[8])
	return result

# monitor name passed as arg
def monitor_0(circuit,engine,args,line):
	return dss.get_monitor_mode_0(engine,circuit,line[8])	
	
def monitor_1(circuit,engine,args,line):
	return dss.get_monitor_mode_1(engine,circuit,line[8])	
	
def storage(circuit,engine,args,line):
	return dss.energyStorage(engine,line[6],line[8],line[9],line[10])

def fault(circuit,engine,args,line):
	return dss.fault(engine,line[6],line[8],line[9],line[10])

def get_load_value(circuit,engine,args,line):
	return dss.getL(line[6],line[5],args.et)

def get_gen_value(circuit,engine,args,line):
	return dss.getG(line[6],line[5],args.et)



## Add custom handlers here! ##

'''
def example(circuit,engine,args,line):
	return ??

'''




'''
end

'''