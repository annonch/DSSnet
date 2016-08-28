#####################
# pre/post handling #
#      Events       #
#####################
#  channon@iit.edu  #
#####################
#      DSSnet       #
#    Version 2.0    #
#####################

#this file holds preprocessing events for custom synchronization requests 
#add pre and post procesing events here

#preprocessing



def pre_load(line):
	result = 'update_controllable_loads(line[6],line[8])'
	return result
'''
def pre_load(line):
	function_name='update_controllable_loads'
	*args = line[6],line[8]
'''
def pre_gen(line):
	result = 'update_controllable_gens(line[6],line[8])'
	return result

def pre_pmu(line):
	result= 'read_monitor(line[6])'	
	return result

#postprocessing

def post_load(line,result):
	return result	

def post_gen(line,result):
	return result

def post_pmu(line,result):
	#print (result) 	
	return result

#smt

def pre_energyStorage(line):
	return 'energyStorage("ES",line[8],line[9],line[10])'

def pre_load_report(line):
	result = 'load.updateL(line[6],line[5])'
	return result
	
def pre_gen_report(line):
	result = 'get_power_sensor(line[8])'#get_gen(line[6],line[5])'
	return result

def post_energyStorage(line,result):
	return result

def	post_load_report(line,result):
	return result

def post_gen_report(line,result):
	#print(result)
	return result
