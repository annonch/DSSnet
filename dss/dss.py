#API for DSSnet -> openDSS

# channon@iit.edu

import math

# read in files for generators and loads with dynamic values

Gen_files = []
Load_files = []

with open('C:\DSS\DSSnet\dss\IED.config','r') as ins:
		for line in ins:
			lin = line.split()
			if lin[0] == 'load':
				Load_files.append('%s%s'%(lin[1],'.csv'))
			if lin[0] == 'gen':
				Gen_files.append('%s%s'%(lin[1],'.csv'))	


## decorator for setting static function variables ##
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func,k,kwargs[k])
        return func
    return decorate

## begin API ##


def get_monitor_mode_0(engine,circuit,name):
    DSSMonitors = circuit.Monitors
    direct(engine,'sample')
    DSSMonitors.Name = name
    length_of_channel = len(DSSMonitors.Channel(1))-1
    time=DSSMonitors.dblHour[len(DSSMonitors.dblHour)-1]
    v1 = DSSMonitors.Channel(1)[length_of_channel]
    vang1 = DSSMonitors.Channel(2)[length_of_channel]
    v2 = DSSMonitors.Channel(3)[length_of_channel]
    vang2 = DSSMonitors.Channel(4)[length_of_channel]
    v3 = DSSMonitors.Channel(5)[length_of_channel]
    vang3 = DSSMonitors.Channel(6)[length_of_channel]
    i1 = DSSMonitors.Channel(7)[length_of_channel]
    iang1 = DSSMonitors.Channel(8)[length_of_channel]
    i2 = DSSMonitors.Channel(9)[length_of_channel]
    iang2 = DSSMonitors.Channel(10)[length_of_channel]
    i3 = DSSMonitors.Channel(11)[length_of_channel]
    iang3 = DSSMonitors.Channel(12)[length_of_channel]
    freq = DSSMonitors.dblFreq[len(DSSMonitors.dblFreq)-1]

    return ('%d %d %d %d %d %d %d %d %d %d %d %d %d %d' % 
            ( freq, 
                v1, vang1,
                v2, vang2,
                v3, vang3,
                i1, iang1,
                i2, iang2,
                i3, iang3,
                time))
	

def get_monitor_mode_1(engine,circuit,name):
    DSSMonitors = circuit.Monitors
    direct(engine,'sample')
    DSSMonitors.name = name
      
    s1 = DSSMonitors.Channel(1)[len(DSSMonitors.Channel(1))-1]
    s2 = DSSMonitors.Channel(3)[len(DSSMonitors.Channel(3))-1]
    s3 = DSSMonitors.Channel(5)[len(DSSMonitors.Channel(5))-1]
    a1 = DSSMonitors.Channel(2)[len(DSSMonitors.Channel(2))-1]
    a2 = DSSMonitors.Channel(4)[len(DSSMonitors.Channel(4))-1]
    a3 = DSSMonitors.Channel(6)[len(DSSMonitors.Channel(6))-1]

    p1 = s1*math.cos(math.radians(a1))
    p2 = s2*math.cos(math.radians(a2))
    p3 = s3*math.cos(math.radians(a3))
    #print('S: %s %s %s ' %(s1,s2,s3))
    #print('A: %s %s %s ' %(a1,a2,a3))
    #print('P: %s %s %s ' %(p1,p2,p3))
    #engine.Text.Command='export monitor mon_wind_gen'
    return ('%d %d %d %d %d %d %d %d %d' 
    		% (s1,s2,s3,a1,a2,a3,p1,p2,p3))

# modes 2 & 3 not used yet
def get_monitor_mode_2(name):
	pass

def get_monitor_mode_3(name):
	pass

def fault(engine,name,phase,node1,node2):
    if node2 == 'a' :
        print('New Fault.%s phases=%s Bus1=%s' % (name,phase,node1))
        engine.Text.Command='New Fault.%s phases=%s Bus1=%s' % (name,phase,node1)
    else:
        engine.Text.Command='New Fault.%s phases=%s Bus1=%s Bus2=%s' % (name,phase,node1,node2)
        print('New Fault.%s phases=%s Bus1=%s Bus2=%s' % (name,phase,node1,node2))
    return 0

def energyStorage(engine,name, p1,p2,p3):
    #we assume that energy storage devices are 3 phase
    engine.Text.Command = 'Storage.%s1.kW = %s'% (name , str(float(p1)))
    engine.Text.Command = 'Storage.%s2.kW = %s'% (name , str(float(p2)))
    engine.Text.Command = 'Storage.%s3.kW = %s'% (name , str(float(p3)))
    return 0 

def direct(engine,cmd):
    engine.Text.Command=cmd
    
def updateTime(engine,dt,loads,gens,end_time):
    cmd='set sec=%s' % str(float(dt)-1.0)
    engine.Text.Command=cmd
    updateLoads(engine,dt,loads,end_time)
    updateGeneration(engine,dt,gens,end_time)
    engine.Text.Command='solve'

def exportMonitors(engine,monitors):
    #print('hi')
    for m in monitors:
        direct(engine,'export monitor %s' % m)
        print('export monitor %s' % m)

def updateLoads(engine,dt,loads,end_time):
    for l in loads:
        updateL(engine,l,dt,end_time)
	
def updateGeneration(engine,dt,gens,end_time):
	for g in gens:
		updateG(engine,g,dt,end_time)
	
def readfile(f):
	data=[]
	with open(f,'r') as ins:
		for line in ins:
			data.append(line)
	return data

def readfiles(files):
    data={}
    for f in files:
    	data[f.split('.')[0]]=readfile(f)
       
    return data

@static_vars(data=readfiles(Gen_files))
def getG(G,t,end_time):
    try:
        position = int(float(t)* float(len(getG.data[G]))/float(end_time))
        if position >= len(getG.data[G]):
            position = len(getG.data[G])-1
        pu_gval = float(getG.data[G][int(position)]) 
    except KeyError:
        print ('key error with gen: %s ' % gen)
	#print ('pu: %s' % pu_gval)
	#print('total power: %s' % pu_val)
	#return 1500
    return pu_gval

@static_vars(data=readfiles(Load_files))
def getL(L,t,end_time):
    #print (t)
    #print((len(getL.data[L]))) 
    #print ((end_time))


    position = int(float(t)* float(len(getL.data[L]))/float(end_time))
    if position >= len(getL.data[L]):
        position = len(getL.data[L])-1
    pu_gval = float(getL.data[L][int(position)]) 
	
	#print ('pu: %s' % pu_gval)
	#print('total power: %s' % pu_val)
	#return 1500
    return pu_gval

def updateL(engine,L,t,end_time,val=None):
    if val == None:
        val = getL(L,t,end_time)
    engine.text.Command = 'load.%s.kW=%s '%(str(L),str(val))	

def updateG(engine,G,t,end_time,val=None):
    if val == None:
        val = getG(G,t,end_time)
    engine.text.Command = 'generator.%s.kW=%s '%(str(G),str(val))	

@static_vars(previous_time=float(-0.5))
def get_up_to_date(engine,t,args,loads,gens): # solve for time step up until previous time
    if get_up_to_date.previous_time < 0.0:
        get_up_to_date.previous_time = t
        #print('You should only see this once! %s'%type(get_up_to_date.previous_time))
        return 0

    time=t#-0.0005 # force round down I dont think we need cuz of round function
    iterations = int((round(time,3)-round(get_up_to_date.previous_time,3))/args.timestep) 
    
    for i in range(iterations):
        dt =get_up_to_date.previous_time + args.timestep
        updateTime(engine,dt,loads,gens,args.et)
        direct(engine,'sample')
        get_up_to_date.previous_time = dt    
    
    if get_up_to_date.previous_time > args.et:

        return('end')


