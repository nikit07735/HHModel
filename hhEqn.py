import numpy as np
import matplotlib.pyplot as plt

class HHModel:
    class Gate:
        def __init__(self):
            # Instance attributes, not class attributes!
            self.alpha = 0.0
            self.beta = 0.0
            self.state = 0.0
        
        def update(self, deltaT):
            self.state += deltaT * (self.alpha * (1 - self.state) - self.beta * self.state)
         
        def equilibriumState(self):
            self.state = self.alpha / (self.alpha + self.beta)

    # Reversal potentials (Modern convention: Rest ~ -70mV)
    # Using the standard relative offsets:
    EK, ENa, EL = -12, 115, 10.6 
    gMaxK, gMaxNa, gMaxL = 36, 120, 0.3
    Cm = 1.0

    def __init__(self, startingVoltage=0):
        self.V = startingVoltage
        self.n = self.Gate()
        self.m = self.Gate()
        self.h = self.Gate()
        self.UpdateGate(startingVoltage)
        self.n.equilibriumState()
        self.m.equilibriumState()
        self.h.equilibriumState()
    
    def UpdateGate(self, V):
        # We use a small epsilon to avoid division by zero
        eps = 1e-7

        # n-gate (Potassium activation)
        n_num = 0.01 * (10 - V)
        n_den = np.exp((10 - V) / 10) - 1
        self.n.alpha = n_num / (n_den + eps) if abs(n_den) < eps else n_num / n_den
        self.n.beta = 0.125 * np.exp(-V / 80)

        # m-gate (Sodium activation)
        m_num = 0.1 * (25 - V)
        m_den = np.exp((25 - V) / 10) - 1
        self.m.alpha = m_num / (m_den + eps) if abs(m_den) < eps else m_num / m_den
        self.m.beta = 4 * np.exp(-V / 18)

        # h-gate (Sodium inactivation)
        self.h.alpha = 0.07 * np.exp(-V / 20)
        self.h.beta = 1 / (np.exp((30 - V) / 10) + 1)

    def UpdateChannels(self, stimI, deltaT):
        # Calculate currents
        self.IK = self.gMaxK * (self.n.state**4) * (self.V - self.EK)
        self.INa = self.gMaxNa * (self.m.state**3) * self.h.state * (self.V - self.ENa)
        self.IL = self.gMaxL * (self.V - self.EL)
        
        # dv/dt = (I_stim - I_ionic) / Cm
        dV = (stimI - self.IK - self.INa - self.IL) / self.Cm
        self.V += deltaT * dV

    def Iterate(self, stimI, deltaT):
        self.UpdateGate(self.V)
        self.UpdateChannels(stimI, deltaT)
        self.m.update(deltaT)
        self.n.update(deltaT)
        self.h.update(deltaT)

# Simulation
model = HHModel(startingVoltage=0)
t = np.linspace(0, 50, 10000) # Increased resolution
V_history = np.zeros(len(t))
dt = t[1] - t[0]

for i in range(len(t)):
    I = 15 if 5 < t[i] < 30 else 0
    model.Iterate(I, dt)
    V_history[i] = model.V

plt.figure(figsize=(10, 4))
plt.plot(t, V_history)
plt.title('Hodgkin-Huxley Action Potential (Relative Voltage)')
plt.ylabel('Voltage Displacement (mV)')
plt.xlabel('Time (ms)')
plt.grid(True)
plt.show()