# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:51:00 2021

@author: juliu
"""

import numpy as np
import matplotlib.pyplot as plt
import tqdm

G = 6.67e-11
c = 299792458

fig, ax = plt.subplots()

class System:
    def __init__(self, M, r_min, r_max, h, N=int(1e3)):
        # Important Note: r_min and r_max are in unit of r_s!!
        # h is in unit of 3**0.5*r_s*c
        self.M = M
        self.r_min = r_min
        self.r_max = r_max
        self.r_s = 2*G*M/c**2
        self.h = 3**0.5*self.r_s*c*h
        self.r_p = self.h**2/c**2*(1 + (1-3*self.r_s**2*c**2/self.h**2)**0.5 )/self.r_s
        self.r_m = self.h**2/c**2*(1 - (1-3*self.r_s**2*c**2/self.h**2)**0.5 )/self.r_s
        self.r = np.linspace(r_min*self.r_s, r_max*self.r_s, N)
        self.V = self.h**2/(2*self.r**2) * (1 - self.r_s/self.r) - G*M/self.r
        self.V_c = self.h**2/(2*self.r**2)
        self.V_g = -G*M/self.r
        self.V_GR = self.h**2/(2*self.r**2) * (-self.r_s/self.r)
    def plot(self, fig, ax, name="Veff.png", save=True, xylims=None):
        ax.plot(self.r/self.r_s, self.V,    color='b', label="$V_{\mathrm{eff}}$")
        ax.plot(self.r/self.r_s, self.V_c,  color='deepskyblue', linestyle = 'dashed', label="Centrifugal")
        ax.plot(self.r/self.r_s, self.V_g,  color='deepskyblue', linestyle = 'dotted', label="Newtonian gravity")
        ax.plot(self.r/self.r_s, self.V_GR, color='deepskyblue', linestyle = '-.', label="GR effect")
        ax.axvline(self.r_p/self.r_s, 0, 1, color='lightgray', linestyle = 'solid', label="$r_{\mathrm{+}}$") # 1.5r_s
        ax.axvline(self.r_m/self.r_s, 0, 1, color='lightgray', linestyle = 'dashed', label="$r_{\mathrm{-}}$") # 1.5r_s
        ax.set_xlabel("$r/r_s$")
        ax.set_ylabel("$V_{\mathrm{eff}}~(m^2/s^2)$")
        ax.legend(loc='upper right')
        ax.set_title("M = {:.2e}, h = {:.2e}".format(self.M, self.h))
        if xylims == None:
            ax.set_xlim(self.r_min, self.r_max)
            ax.set_ylim(np.min(self.V) + (np.max(self.V) - np.min(self.V))*0.1, np.max(self.V) + (np.max(self.V) - np.min(self.V))*0.9)
        else:
            ax.set_xlim(xylims[0], xylims[1])
            ax.set_ylim(xylims[2], xylims[3])
        #plt.tight_layout()
        if save:
            plt.savefig(name, dpi=200)
        else:
            plt.show()
    def estimate_xylims(self):
        Xmin = self.r_min
        Xmax = self.r_max
        Ymin = np.min(self.V) + (np.max(self.V) - np.min(self.V))*0.1
        Ymax = np.max(self.V) + (np.max(self.V) - np.min(self.V))*0.9
        return [Xmin, Xmax, Ymin, Ymax]

BH_lim = System(2e30, 1, 10, 1.5)
XYlims = BH_lim.estimate_xylims()

for i, h in tqdm.tqdm(enumerate(np.concatenate((np.linspace(2, 1, 60), np.ones(10))))):
    BH1 = System(2e30, 1, 10, h)
    BH1.plot(fig, ax, 
             "./images/Veff_{:04d}.png".format(i), 
             xylims = XYlims,
             save=True)
    ax.cla()
