# -*- coding: utf-8 -*-
"""Poisson Eq, Electric Dipole (In Progress)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UFO9h4DQH4CkPJEBom8riQen-UryM2Ku
"""

import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import scipy.optimize

grid = np.zeros((80,80,80))

charge = np.zeros((80,80,80))

dh = .5

#.5 charge density
charge[41][40][40] = 2/(dh**3)

#-.5 charge density
charge[39][40][40] = -2/(dh**3)

def potential(grid, charge):

  lap = 0
  grid1 = grid.copy()

  for a in range(1, 79):

    for b in range(1, 79):

      for c in range(1, 79):

        if((((a-40))**2 + ((b-40))**2 + ((c-40))**2) >= 40**2):
          grid1[a][b][c] = 0

        else:
          grid1[a][b][c] = (grid[a+1][b][c] + grid[a-1][b][c] + grid[a][b+1][c] + grid[a][b-1][c] + grid[a][b][c+1] + grid[a][b][c-1])/6 + (charge[a][b][c]*dh**2)/6

          lap = lap + abs(grid1[a][b][c] - grid[a][b][c])

  return grid1, lap

"""###CONVERGENCE LIMIT:"""

q = 0
d = 100

while np.any(d > 0.7):

    grid, d = potential(grid, charge)
    q = q + 1

print(d, q)

xyz = []
x = []

for i in range(1,79):
  xyz.append(grid[i][i][i])
  x.append((i-40)/2)

plt.plot(x, xyz)
plt.xlabel('radius')
plt.ylabel('V')
plt.show()

x = np.linspace(30,49,20).astype(int)

y = np.linspace(30,49,20).astype(int)

X, Y = np.meshgrid(x,y)

def arb(i,j):
  return grid[i][j][40]

val = []

for i in range(len(X)):
  val.append([])

  for j in range(len(X[i])):
    val[i].append(arb(X[i][j],Y[i][j]))

print(X)
print(Y)

plt.contour(X,Y, val, 500, colors = 'blue')

import numpy as np

# Define constants
Q = 2  # point charge
a = 1  # distance between charges
e0 = 8.8541e-12  # vacuum permittivity
R = 20  # boundary radius
delta = 1  # grid spacing
tolerance = 1e-5  # numerical tolerance

# Define grid
x = np.arange(-R, R+delta, delta)
y = np.arange(-R, R+delta, delta)
z = np.arange(-R, R+delta, delta)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Initialize potential array
V = np.zeros_like(X)

# Define functions for calculating distance and potential
def distance(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def potential(x, y, z):
    return Q / (4*np.pi*e0*distance(x, y, z, a/2, 0, 0)) \
           - Q / (4*np.pi*e0*distance(x, y, z, -a/2, 0, 0))

# Implement Jacobi relaxation algorithm
max_iterations = 5
for iteration in range(max_iterations):
    V_old = V.copy()
    for i in range(1, len(x)-1):
        for j in range(1, len(y)-1):
            for k in range(1, len(z)-1):
                if distance(x[i], y[j], z[k], 0, 0, 0) < R:
                    V[i,j,k] = (V_old[i+1,j,k] + V_old[i-1,j,k] \
                                + V_old[i,j+1,k] + V_old[i,j-1,k] \
                                + V_old[i,j,k+1] + V_old[i,j,k-1]) / 6.0
                    V[i,j,k] = V[i,j,k] + potential(x[i], y[j], z[k])
    if np.max(np.abs(V - V_old)) < tolerance:
        print(f'Converged after {iteration} iterations')
        break

import matplotlib.pyplot as plt

# Define constants
Q = 2  # point charge
a = 1  # distance between charges
e0 = 8.8541878128e-12  # vacuum permittivity
R = 20  # boundary radius
delta = 0.01  # grid spacing
tolerance = 1e-5  # numerical tolerance

# Define grid
x = np.arange(-R, R+delta, delta)
y = np.arange(-R, R+delta, delta)
z = np.arange(-R, R+delta, delta)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Initialize potential array
V = np.zeros_like(X)

# Define functions for calculating distance and potential
def distance(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

def potential(x, y, z):
    return Q / (4*np.pi*e0*distance(x, y, z, a/2, 0, 0)) \
           - Q / (4*np.pi*e0*distance(x, y, z, -a/2, 0, 0))

# Implement Jacobi relaxation algorithm
max_iterations = 10
for iteration in range(max_iterations):
    V_old = V.copy()
    for i in range(1, len(x)-1):
        for j in range(1, len(y)-1):
            for k in range(1, len(z)-1):
                if distance(x[i], y[j], z[k], 0, 0, 0) < R:
                    V[i,j,k] = (V_old[i+1,j,k] + V_old[i-1,j,k] \
                                + V_old[i,j+1,k] + V_old[i,j-1,k] \
                                + V_old[i,j,k+1] + V_old[i,j,k-1]) / 6.0
                    V[i,j,k] = V[i,j,k] + potential(x[i], y[j], z[k])
    if np.max(np.abs(V - V_old)) < tolerance:
        print(f'Converged after {iteration} iterations')
        break

# Plot equipotential lines
fig, ax = plt.subplots()
levels = np.arange(-0.2, 0.2, 0.01)
ax.contour(X[:,:,int(len(z)/2)], Y[:,:,int(len(z)/2)], V[:,:,int(len(z)/2)], levels=levels)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal')
plt.show()

# Plot V(r) for x=y=z
r = np.sqrt(X**2 + Y**2 + Z**2)
V_r = V[int(len(x)/2), int(len(y)/2), int(len(z)/2):]
fig, ax = plt.subplots()
ax.plot(r[int(len(x)/2), int(len(y)/2), int(len(z)/2):], V_r)
ax.set_xlabel('r')
ax.set_ylabel('V')
plt.show()

# Define constants and parameters
Q = 2.0
a = 1.0
R = 20.0
N = 401
delta = 0.1
tolerance = 1e-6

# Initialize potential grid
V = np.zeros((N, N, N))

# Set boundary conditions
x = np.linspace(-a - delta, a + delta, N)
y = np.linspace(-a - delta, a + delta, N)
z = np.linspace(-a - delta, a + delta, N)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
R = np.sqrt(X**2 + Y**2 + Z**2)
V[R >= R[-1,0,0]] = 0.0

# Solve Poisson equation using Jacobi relaxation
delta2 = delta**2
for k in range(10000):
    V_old = V.copy()
    V[1:-1,1:-1,1:-1] = (V[:-2,1:-1,1:-1] + V[2:,1:-1,1:-1] +
                         V[1:-1,:-2,1:-1] + V[1:-1,2:,1:-1] +
                         V[1:-1,1:-1,:-2] + V[1:-1,1:-1,2:]) / 6
    diff = np.abs(V - V_old).max()
    if diff < tolerance:
        print(f'Converged after {k} iterations')
        break

# Plot potential
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X[:,:,N//2], Y[:,:,N//2], Z[:,:,N//2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

import numpy as np

# Define constants
Q = 2.0
a = 1.0
e0 = 8.85418782e-12

# Define grid size and spacing
n = 100
h = 2.0 / n

# Initialize potential array
phi = np.zeros((n, n, n))

# Set boundary conditions
for i in range(n):
    for j in range(n):
        for k in range(n):
            if i == n // 2 - 1 and j == n // 2 and k == n // 2:
                phi[i, j, k] = Q / (4 * np.pi * e0 * a)
            elif i == n // 2 and j == n // 2 and k == n // 2:
                phi[i, j, k] = -Q / (4 * np.pi * e0 * a)

# Perform Jacobi relaxation
delta = 1.0
while delta > 1e-5:
    old_phi = phi.copy()
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            for k in range(1, n - 1):
                phi[i, j, k] = (old_phi[i+1, j, k] + old_phi[i-1, j, k] +
                                old_phi[i, j+1, k] + old_phi[i, j-1, k] +
                                old_phi[i, j, k+1] + old_phi[i, j, k-1]) / 6
    delta = np.max(np.abs(phi - old_phi))

# Print the potential at the center of the dipole
print("Potential at center:", phi[n//2, n//2, n//2])

import numpy as np
import matplotlib.pyplot as plt

# Constants
Q = 2 # point charge
e0 = 8.854e-12 # permittivity of free space
a = 1 # distance between charges
L = 20 # box size
N = 101 # number of grid points
dx = L / (N - 1) # grid spacing

# Define the grid
x = np.linspace(-L/2, L/2, N)
y = np.linspace(-L/2, L/2, N)
z = np.linspace(0, L, N)
X, Y, Z = np.meshgrid(x, y, z)

# Initial potential distribution
V = np.zeros((N, N, N))

# Boundary conditions
V[0,:,:] = 0 # x=0 plane
V[-1,:,:] = 0 # x=L plane
V[:,0,:] = 0 # y=0 plane
V[:,-1,:] = 0 # y=L plane
V[:,:,0] = 0 # z=0 plane
V[:,:,-1] = 0 # impose V(R)=0 at a large distance R=20 or so

# Define a function to calculate the charge density
def rho(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    return Q * (np.abs(x-a/2)/r - np.abs(x+a/2)/r**3) / e0

# Jacobi relaxation method
tolerance = 1e-5
max_iterations = 100
for iteration in range(max_iterations):
    V_old = V.copy()
    for i in range(1, N-1):
        for j in range(1, N-1):
            for k in range(1, N-1):
                V[i,j,k] = (V[i+1,j,k] + V[i-1,j,k] +
                            V[i,j+1,k] + V[i,j-1,k] +
                            V[i,j,k+1] + V[i,j,k-1] +
                            dx**2 * rho(x[i], y[j], z[k])) / 6

# Plot the potential
plt.figure()
plt.imshow(V[:,:,50], extent=(-L/2, L/2, -L/2, L/2))
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()
plt.show()

x = np.linspace(30,49,20).astype(int)
y = np.linspace(30,49,20).astype(int)

X, Y = np.meshgrid(x,y)

def f(i,j):
  return Graph[i][j][40]

values = []
for i in range(len(X)):
  values.append([])
  for j in range(len(X[i])):
    values[i].append(f(X[i][j],Y[i][j]))

plt.contour(X,Y,values,1000,colors = 'blue')