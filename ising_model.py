# -*- coding: utf-8 -*-
"""Ising Model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yefipBd8s7fSSbTDl2_eXr6pUeFbgny7
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def spinsfunc(n):

    spins = np.random.choice([-1, 1], size=(n, n))
    return spins

def energy(spins, J):

    E = 0

    for i in range(len(spins)):
        for j in range(len(spins)):

            s = spins[i][j]

            #neighbor spin
            ns = spins[(i+1)%len(spins)][j] + spins[(i-1)%len(spins)][j] + spins[i][(j+1)%len(spins)] + spins[i][(j-1)%len(spins)]
            #energy
            E = E + -J * s/2 * ns

    return E

def metro(spins, J, T):

    b = 1/T

    for i in range(len(spins)):

        for j in range(len(spins)):

            s = spins[i][j]
            ns = spins[(i+1)%len(spins)][j] + spins[(i-1)%len(spins)][j] + spins[i][(j+1)%len(spins)] + spins[i][(j-1)%len(spins)]
            dE = 2*J * s * ns

            if dE < 0 or np.exp(-b*dE) > np.random.rand():
                spins[i][j] = -s

    return spins

def avg_sim(n, J, T, step):

    spins = spinsfunc(n)
    M = np.zeros(step)

    for i in range(step):
        spins = metro(spins, J, T)
        M[i] = np.abs(np.sum(spins)) / n**2

    return M.mean()

# parameters
n = 20
J = 2 #interaction strength
step = 1000 # monte carlo sweeps

temps = np.linspace(0, 10, 50)

# Simulate the Ising model at each temperature
mags = [avg_sim(n, J, T, step) for T in temps]

#function for fitting
#x0 is the critical temperature where the curve changes concavity
def arcfit(x, k, w, x0, y0):
    return k * np.arctan(w*(x-x0)) + y0

plt.plot(temps, mags, '.')
plt.xlabel('Temperature')
plt.ylabel('Magnetization per spin')


p0 = [1, 1]
p0.append(0.5*(max(temps) + min(temps)))
p0.append(0.5*(max(mags) + min(mags)))

fit_temps = []
fit_mags = []


#this is to exclude the stray data points that skew the curve and are caused by randomized error
for t, m in zip(temps, mags):

    if t < 3 and m < 0.9:
        continue

    fit_temps.append(t)
    fit_mags.append(m)

out = curve_fit(arcfit, fit_temps, fit_mags, p0=p0, full_output=True)
copt = out[0]

xfit = temps = np.linspace(0, 10, 50)
yfit = arcfit(xfit, *copt)

plt.plot(xfit, yfit, 'r:')

print('Crit. Temp = {:1.3f}'.format(copt[2]))

Tc = 2.0/np.log(1.0 + np.sqrt(2))*J

step = 500
temps = np.linspace(0.9*Tc, Tc, 30)
B_list = []

# calculate magnetization per spin for different lattice sizes
mags = np.zeros(len(temps))

for i in range(len(temps)):
    T = temps[i]
    mag = avg_sim(20, J, T, step)
    mags[i] = mag

plt.plot(temps, mags, '.', label=f'n=20')
plt.xlabel('Temperature')
plt.ylabel('Magnetization per spin')
plt.legend()

#fit log plot, find beta
log_mags = np.log(mags)
log_temps = np.log(Tc - temps)
valid = np.where((log_mags > np.log(.1)) & (log_temps > np.log(0.1)))
p0 = [1, 1]
popt, _ = curve_fit(lambda x, c, b: c + b*x, log_temps[valid], log_mags[valid], p0=p0)
B = popt[1]
B_list.append(B)

print(f'n = 20, B = {B:.3f}')

Tc = 2.0/np.log(1.0 + np.sqrt(2))*J

step = 1000
temps = np.linspace(0.9*Tc, Tc, 30)
B_list = []

# calculate magnetization per spin for different lattice sizes
mags = np.zeros(len(temps))

for i in range(len(temps)):
    T = temps[i]
    mag = avg_sim(40, J, T, step)
    mags[i] = mag

plt.plot(temps, mags, '.', label=f'n=40')
plt.xlabel('Temperature')
plt.ylabel('Magnetization per spin')
plt.legend()

#fit log plot, find beta
log_mags = np.log(mags)
log_temps = np.log(Tc - temps)
valid = np.where((log_mags > np.log(.1)) & (log_temps > np.log(0.1)))
p0 = [1, 1]
popt, _ = curve_fit(lambda x, c, b: c + b*x, log_temps[valid], log_mags[valid], p0=p0)
B = popt[1]
B_list.append(B)

print(f'n = 40, B = {B:.3f}')

a = .117/.153
print('B_n=20 / B_n=40  = ', a)

"""#Part B"""

n=20
J=2

def avg_sim_energy(n, J, T, step):
    spins = spinsfunc(n)
    E = np.zeros(step)

    for i in range(step):
        spins = metro(spins, J, T)
        E[i] = energy(spins, J) / n**2

    return E.mean()

Ts = np.linspace(0, 10, 50)

steps = 1000

# compute energy per spin for each temperature
energy_per_spin = np.array([avg_sim_energy(n, J, T, steps) for T in Ts])

plt.plot(Ts, energy_per_spin, '.')
plt.xlabel('Temperature')
plt.ylabel('Energy per spin')

"""###Above the critical temperature, $T_c$, we see consistency with the physical interpretation of the Ising model as a model of ferromagnetism and paramagnetism, where spins tend to align with their neighbors to minimize energy. At higher temperatures, the system has a tendency to minimize its energy by having spins pointing in random directions. At low temperatures the system tends to have a lower energy by having spins aligned.

#Part C
"""

def en(spins, J):

    E = 0

    for i in range(len(spins)):
        for j in range(len(spins)):

            s = spins[i][j]

            #neighbor spin
            ns = spins[(i+1)%len(spins)][j] + spins[(i-1)%len(spins)][j] + spins[i][(j+1)%len(spins)] + spins[i][(j-1)%len(spins)]
            #energy
            E = E + -J * s * ns

    return E

def specific_heat(n, J, Ts, step):
    Es = np.zeros((len(Ts), step))
    Ms = np.zeros((len(Ts), step))
    Cs = np.zeros(len(Ts))

    for t in range(len(Ts)):
        spins = spinsfunc(n)
        for i in range(step):
            spins = metro(spins, J, Ts[t])
            if step > 100:
              Es[t][i] = energy(spins, J)

        # compute heat capacity
        E_mean = np.mean(Es[t])
        E2_mean = np.mean(Es[t]**2)
        Cv = abs(E2_mean/(step) - (E_mean**2)/(step)**2) / (Ts[t]**2)
        Cs[t] = Cv / (n**2)

    return Cs

# set parameters
n = 10
J = 2
Ts = np.linspace(3, 7.5, 100)
step = 500

# compute and plot specific heat
Cs = specific_heat(n, J, Ts, step)
plt.plot(Ts, Cs, '-', label=f'n={n}')

plt.xlabel('Temperature')
plt.ylabel('Specific heat per spin')
plt.legend()
plt.show()

def Monte_Carlo(T,state):
  for i in range(len(state)):
    for j in range(len(state[i])):
      s = state[i][j]
      nb = state[(i+1)%len(state)][j] + state[(i-1)%len(state)][j] + state[i][(j+1)%len(state)] + state[i][(j-1)%len(state)]
      E =  2 * 2 * s * nb
      if E < 0 or np.random.rand() < np.exp(-E/T):
        state[i][j] = -s

  #plt.matshow(state)
  return abs(sum(sum(state,[]))),state

def create_matrix(n):
  return [[(np.random.randint(2)-(1/2))*2 for i in range(n)] for j in range(n)]

size = [10,20,30,100]
Cmax = []
for i in size:
  Temps = np.linspace(1,6.0, 10)
  avg_s = []
  avg_e = []
  for T in Temps:
    s= []
    e1 = []
    state = create_matrix(i)
    for k in range(500):

      M, state = Monte_Carlo(T,state)
      if k > 100:
        e1.append(energy(state, 2))
    avg_e.append((np.var(e1)**2)/(T**2)/(400*i**2))

  plt.plot(Temps,avg_e,  'o')
  plt.show()

  Cmax.append(max(avg_e))
  print(Cmax)

nvals = [100]
Cmax = []

for i in nvals:

  temps = np.linspace(2, 6.0, 10)
  avg_s = []
  avg_E = []

  for T in temps:

    s = []
    energy1 = []
    spins = spinsfunc(i)

    for k in range(200):

      spins1 = metro(T, 2, spins)

      if l > 10:
        energy1.append(energy(spins1, 2))

    avg_E.append((np.var(energy1)**2)/(T**2)/(400*i**2))

  plt.plot(temps, avg_E,  '-')
  plt.show()

  Cmax.append(max(avg_E))
  print(Cmax)

CN=[]
for i in range(len(Cmax)):
  CN.append(Cmax[i]/(size[i]**2))

"""#PART D"""

def magnetize(T,H,spins):
  for i in range(len(state)):
    for j in range(len(state[i])):
      s = state[i][j]
      nb = state[(i+1)%len(state)][j] + state[(i-1)%len(state)][j] + state[i][(j+1)%len(state)] + state[i][(j-1)%len(state)]
      E = 2 * 2 * s * nb - 2 * H * s
      if E < 0 or np.random.rand() < np.exp(-E/T):
        state[i][j] = -s

  #plt.matshow(state)
  return (sum(sum(state,[]))),state

def energyH(spins, J, H):

    E = 0

    for i in range(len(spins)):
        for j in range(len(spins)):

            s = spins[i][j]
            ns = spins[(i+1)%len(spins)][j] + spins[(i-1)%len(spins)][j] + spins[i][(j+1)%len(spins)] + spins[i][(j-1)%len(spins)]
            E = E - J * s/2 * ns - H * s

    return E

def metroH(spins, J, H, T):

    b = 1/T

    for i in range(len(spins)):
        for j in range(len(spins)):

            s = spins[i][j]
            ns = spins[(i+1)%len(spins)][j] + spins[(i-1)%len(spins)][j] + spins[i][(j+1)%len(spins)] + spins[i][(j-1)%len(spins)]
            dE = 2 * J * s/2 * ns + 2 * H * s

            if dE < 0 or np.exp(-b*dE) > np.random.rand():
                spins[i][j] = -s

    return spins

def mag_vs_H(n, J, T, H_min, H_max, H_step):

    spins = spinsfunc(n)
    M = np.zeros(int((H_max - H_min) / H_step) + 1)
    H_list = np.arange(H_min, H_max + H_step, H_step)

    for i, H in enumerate(H_list):
        for j in range(10): #thermalization steps

            spins = metroH(spins, J, H, T)

        M[i] = (np.sum(spins)) / n**2

    plt.plot(H_list, M, '.')
    plt.xlabel("External magnetic field H")
    plt.ylabel("Magnetization per spin")
    plt.show()

J = 2
Tc = 4.5
n = 20
H_min = -10
H_max = 10
H_step = 0.01
T1 = 1.5 * Tc
T2 = Tc / 3
mag_vs_H(n, J, T1, H_min, H_max, H_step)
mag_vs_H(n, J, T2, H_min, H_max, H_step)

"""###The hysteresis effect in the latter case ($T_{c}/3$) is not prevelant, which aligns with expectation."""