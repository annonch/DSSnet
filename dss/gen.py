#import 
pu = 1000*1.333
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
		position = len(updateG.data)/(float(end_time)/time_interval)*float(t)*time_interval
		pu_val = float(updateG.data[int(position)]) *pu
		#print('%s' % pu_val)
		return pu_val