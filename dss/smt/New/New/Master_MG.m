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
DSSText.Command = 'set mode=snapshot';
DSSSolution.Solve();
DSSText.Command = 'set mode=dynamics';
DSSSolution.Stepsize =0.01;
gencsv=csvread('WindRamp.csv',0,0);
gen=gencsv(2:end,1);

for t=1:1000 % Normal Operation
  DSSText.Command = ['Generator.gen.kw=' num2str(gen(t)*1000)]; 
  DSSText.Command = ['Load.load1.kw=' num2str(170+rand*5)]; 
  DSSText.Command = ['Load.load1.kvar=' num2str(125+rand*5)];
  DSSText.Command = ['Load.load2.kw=' num2str(230+rand*5)];
  DSSText.Command = ['Load.load2.kvar=' num2str(132+rand*5)];
  DSSText.Command = ['Load.load3.kw=' num2str(170+rand*5)];
  DSSText.Command = ['Load.load3.kvar=' num2str(80+rand*5)];
  DSSText.Command = ['Load.load4.kw=' num2str(128+rand*5)];
  DSSText.Command = ['Load.load4.kvar=' num2str(82+rand*5)];
  
  % [Send Commands to Control Energy Storage Output]
  % [Time Latency Emulated]
  
  DSSSolution.Solve();
  disp(['Seconds Elapsed: ' num2str(DSSSolution.Seconds)])
end

DSSText.Command = 'line.650632.enabled=false'; % Simulate an Islanding Operation

for t=1001:2000 % Operation in an Emergency
  DSSText.Command = ['Generator.gen.kw=' num2str(gen(t)*1000)];
  
  % [Send Commands to Control Energy Storage Output]
  % [Curtail Controllable Loads If Necessary]
  % [Time Latency Emulated]
  
  DSSSolution.Solve();
  disp(['Seconds Elapsed: ' num2str(DSSSolution.Seconds)])
end

% [Examine the Voltag Evolution Curves of Buses 634, 675, 646, 611, 652,
% 680]