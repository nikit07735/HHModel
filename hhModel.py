import numpy as np
import matplotlib.pyplot as plt

class HHModel:
    
    class Gate:
        alpha, beta, state = 0.0, 0.0, 0.0
        
        def update(self, deltaT):
            alphaState = self.alpha * (1-self.state)
            betaState = self.beta * self.state
            self.state += deltaT * (alphaState - betaState)
         
        def equilibriumState(self):
            self.state = self.alpha / (self.alpha + self.beta)
    #constants
    EK, ENa, EKleak = -12, 115, 10.6
    gMaxK, gMaxNa, gMaxKleak = 36, 120, 0.3
    
    n, m, h = Gate(), Gate(), Gate()
    Cm = 1
    V = 0

    def __init__(self, startingVoltage=0):
        self.V = startingVoltage
        self.UpdateGate(startingVoltage)
        self.m.equilibriumState()
        self.n.equilibriumState()
        self.h.equilibriumState()
    
    def UpdateGate(self, V):
        self.n.alpha = .01* ((V + 10) / (np.exp((V+10)/10)-1))
        self.n.beta = 0.125* np.exp(-V/80)

        self.m.alpha = 0.1*((V+25)/(np.exp((V+25)/10)-1))
        self.m.beta = 4*np.exp(-V/18)

        self.h.alpha = .07*np.exp(-V/20)
        self.h.beta = 1/(np.exp((V+30)/10)+1)

    def UpdateChannels(self, stimiI, deltaT):
        self.IK = self.gMaxK * np.power(self.n.state, 4)*(self.V-self.EK)
        self.INa = self.gMaxNa * np.power(self.m.state, 3) * self.h.state *(self.V-self.ENa)
        self.IL = self.gMaxKleak * (self.V - self.EKleak)
        
        sumI = stimiI - self.IK - self.INa - self.IL
        self.V += deltaT * sumI/self.Cm

    def UpdateGateStates(self, deltaT):
        self.m.update(deltaT)
        self.n.update(deltaT)
        self.h.update(deltaT)

    def Iterate(self, stimiI, deltaT):
        self.UpdateGate(self.V)
        self.UpdateChannels(stimiI, deltaT)
        self.UpdateGateStates(deltaT)




model = HHModel()
t = np.linspace(0, 50, 5000)  # 50ms simulation
V = np.zeros(len(t))
dt = t[1] - t[0]

for i in range(1, len(t)):
    I = 30 if 5 < t[i] < 15 else 0  # 10uA pulse 5-15ms
    model.Iterate(I, dt)
    V[i] = model.V

plt.plot(t, V)
plt.ylabel('Voltage')
plt.xlabel('Time (ms)')
plt.show()
        
        