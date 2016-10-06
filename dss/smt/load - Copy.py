import random
total_load = 1000.0
end_time = 10

def updateL(l,t): # L is name of load and t is time
	# should be function of time
	if l == 'load1a' :
		return str(float(t)*100 + 5400) 

	if l == '671' : 
		return str(float(3*1400)-((3/4)* float(t)) + (random.random()*40-20))
	
	if l =='load1':
		p=(float(t)*((.25*total_load)/end_time))+(1/8)*total_load
		return str(p+0.001)
	if l =='load2':
		p=(float(t)*((-.25*total_load)/end_time))+(3/8)*total_load
		return str(p+0.001)
	if l =='load3':	
		p=float(t)*(.5*total_load)/end_time
		return str(p+0.001)
	if l =='load4':
		p=float(t)*(-.5*total_load)/end_time+(1/2)*total_load
		return str(p+0.001)	
