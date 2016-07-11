import random
total_load = 100
end_time = 10

def updateL(l,t):
	if l == 'load1' :
		return str(float(t)*100 + 5400) 


	if l == '671' : 
		return str(float(3*1400)-(3/4* float(t)) + (random.random()*40-20))
	
	if l =='load_1':
		p=t*(.025*total_load)+1/8*total_load
		return str(p)
	if l =='load_2':
		p=t*(-.025*total_load)+3/8*total_load
		return str(p)
	if l =='load_3':
		p=t*(-.05*total_load)
		return str(p)
	if l =='load_4':
		p=t*(.05*total_load)+2/8*total_load
		return str(p)	


