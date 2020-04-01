import numpy as np
import pandas as pd 
import scipy
import matplotlib.pyplot as plt 
from scipy import optimize, interpolate
data = pd.read_csv('../pecaut2013.csv',sep='\s+')
print(data.columns)
index1 = data['Bp-Rp'] != '...'
index2 = data['B-V'] != '...'

data = data[index2][index1]
bp_rp = np.array(data['Bp-Rp'],dtype='float')
msun = np.array(data['Msun'],dtype='float')
print('The range of Bp-Rp is %s to %s' %(bp_rp.min(),bp_rp.max()))

f_xy = interpolate.interp1d(bp_rp,msun)
# def piecewise_linear(x, x0, y0, k1, k2):
# 	# x<x0 ⇒ lambda x: k1*x + y0 - k1*x0
# 	# x>=x0 ⇒ lambda x: k2*x + y0 - k2*x0
#     return np.piecewise(x, [x < x0, x >= x0], [lambda x:k1*(x-x0) + y0, 
#                                    lambda x:k2*(x-x0) + y0])

# p , e = optimize.curve_fit(piecewise_linear, bp_rp, msun)
# print(p)
# xd = np.linspace(-0.3,5,100)
# plt.scatter(bp_rp,msun)
# plt.plot(xd,piecewise_linear(xd,p[0],p[1],p[2],p[3]),c='r')
# plt.show()
# plt.savefig('BV-BPRP.png')
# plt.close()

def gaia_mag_to_bv(gaia_mag:float):
	return f_xy(gaia_mag)

def mass_to_tau(mass:float):      # Wright 2011 Apjs
	logtau = 1.16 - 1.49 * np.log10(mass) - 0.54 * np.log10(mass) ** 2
	return 10 ** logtau 

n50 = pd.read_csv('./OCs/NGC1750/matchgaia.csv')
data = np.array(n50['bp_rp'])
mass = gaia_mag_to_bv(data)
n50['mass'] = mass
tau = mass_to_tau(mass)
n50['tau'] = tau
n50.to_csv('n50_mass_tau.csv')

n58 = pd.read_csv('./OCs/NGC1758/matchgaia.csv')
data = np.array(n58['bp_rp'])
mass = gaia_mag_to_bv(data)
n58['mass'] = mass
tau = mass_to_tau(mass)
n58['tau'] = tau
n58.to_csv('n58_mass_tau.csv')








