import sys
import numpy as np
from scipy.integrate import odeint

G = 9.81

class pendulum:
    # Init the pendulum with the initial conditions
    def __init__(self,angle1, angle2):
        self.L1 = 1
        self.L2 = 1
        self.m1 = 1
        self.m2 = 1
        self.y0 = np.array([angle1, 0, angle2, 0])
        self.y = np.array([])
        self.tmax = 30
        self.dt = 0.01
        self.t = np.arange(0, self.tmax+self.dt, self.dt)
        self.x1 = np.array([])
        self.y1 = np.array([])
        self.x2 = np.array([])
        self.y2 = np.array([])


    #Return the first derivatives of y = theta1, z1, theta2, z2.
    def deriv(self, y, t, L1, L2, m1, m2):
        
        theta1, z1, theta2, z2 = y

        c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

        theta1dot = z1
        z1dot = (m2*G*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
                (m1+m2)*G*np.sin(theta1)) / L1 / (m1 + m2*s**2)
        theta2dot = z2
        z2dot = ((m1+m2)*(L1*z1**2*s - G*np.sin(theta2) + G*np.sin(theta1)*c) + 
                m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
        return theta1dot, z1dot, theta2dot, z2dot


    #return arrays of x and y positions of the pendulum
    def solve(self):
        self.y = odeint(self.deriv, self.y0, self.t, args=(self.L1, self.L2, self.m1, self.m2))
        
        theta1, theta2 = self.y[:,0], self.y[:,2]

        self.x1 = self.L1 * np.sin(theta1)
        self.y1 = -self.L1 * np.cos(theta1)
        self.x2 = self.x1 + self.L2 * np.sin(theta2)
        self.y2 = self.y1 - self.L2 * np.cos(theta2)
        