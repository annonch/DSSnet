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
	return result
