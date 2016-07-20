clc
clear all
close all
DSSObj = actxserver('OpenDSSEngine.DSS');
if~DSSObj.Start(0),
    disp('Unable to start the OpenDSS Engine')
    return
end
DSSText = DSSObj.Text;
DSSCircuit = DSSObj.ActiveCircuit;
DSSElement = DSSObj.ActiveCircuit.ActiveCktElement;
DSSSolution = DSSCircuit.Solution;
DSSText.Command = 'Compile master.dss';
DSSSolution.mode =6;
DSSSolution.Number = 10000;
DSSSolution.Stepsize =0.001;
DSSSolution.Solve();
DSSText.Command = 'plot monitor object=mon_1 Channels=[1, 3, 5] Bases=[2400 2400 2400]';
DSSText.Command = 'plot monitor object=mon_2 Channels=[1, 3, 5]';
% DSSText.Command = 'plot monitor object=mon_3 Channels=[1, 3, 5]';
% DSSText.Command = 'Export monitor mon_3';