import win32com.client
import sys

engine=win32com.client.Dispatch("OpenDSSEngine.DSS")
engine.Start("0")
engine.Text.Command='clear'
circuit = engine.ActiveCircuit

engine.Text.Command='compile ' + sys.argv[1]
engine.Text.Command='set sec =10' #=%d' % (1/360)
engine.Text.Command='solve'
engine.Text.Command='sample'

DSSMonitors=circuit.Monitors
DSSMonitors.saveAll()

DSSMonitors.Name = 'a1'

print(DSSMonitors.dblHour)

print(DSSMonitors.Channel(1))
print(DSSMonitors.Channel(2))
print(DSSMonitors.Channel(3))
print(DSSMonitors.Channel(4))
print(DSSMonitors.Channel(5))
print(DSSMonitors.Channel(6))
print(DSSMonitors.Channel(7))
print(DSSMonitors.Channel(8))
print(DSSMonitors.Channel(9))
print(DSSMonitors.Channel(10))
print(DSSMonitors.Channel(11))
print(DSSMonitors.Channel(12))

engine.Text.Command='show monitor a1'


