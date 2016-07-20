#import 
pu = 1000*1.333
time_interval = 0.001
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
def updateG(G,t):
	if G == ' ' :
		return t*100 + 5400 
	if G == 'gen':
		return updateG.data[int(len(updateG.data)/(end_time/time_interval)*(t*time_interval))]*pu