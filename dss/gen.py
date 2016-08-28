#import 
pu = 2300
end_time = 10
fille = 'wind_gen.csv'

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate



def readWind(fille):
	data=[]
	with open(fille,'r') as ins:
		for line in ins:
			data.append(line)
	return data


@static_vars(data=readWind(fille))
def updateG(G,t,time_interval):
	if G == ' ' :
		return t*100 + 5400 
	if G == 'gen':
		#return 1500
		'''
			position = len(updateG.data)/(float(end_time)/time_interval)*float(t)/time_interval
		if position >= len(updateG.data):
			position = len(updateG.data)-1
		pu_gval = float(updateG.data[int(position)]) 
		
		pu_val = pu_gval*pu
		#print ('pu: %s' % pu_gval)
		#print('total power: %s' % pu_val)
		#return 1500
		#return pu_val
		'''

		position = int(float(t)* float(len(updateG.data))/float(end_time))
		if position >= len(updateG.data):
			position = len(updateG.data)-1
		pu_gval = float(updateG.data[int(position)]) 
		
		pu_val = pu_gval*pu
		#print ('pu: %s' % pu_gval)
		#print('total power: %s' % pu_val)
		#return 1500
		return pu_val