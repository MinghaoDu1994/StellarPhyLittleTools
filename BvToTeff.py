import numpy as np
import pandas as pd


#Input : 
    # B_band: A list of B band mag values
    # V_band: A list of V band mag values
    # B_V_band: A list of B-V band mag values
    # stellar type : None stands for main-sequence, subgiants 
    #                and giants and 'SG' means Supergiants

#Output :
    # Teff : Effective temperature 
    # BC : Bolometric correction

#Calling Method:
    # Choice1 : If you have B band values and V band values
    #           Using BvToTeff(B_band,V_band,None,stellar_type)
    # Choice2: If you just have B-V band values 
    #           Using BvToTeff(None,None,B_V_band,stellar_type)
#

def BvToTeff(B_band = None ,V_band = None ,B_V_band = None, stellar_type = None):
    if B_V_band is None:
        b_band = np.array(B_band)
        v_band = np.array(V_band)
        b_v = b_band - v_band
        logteff = np.zeros(b_band.shape)
        if b_band.shape != v_band.shape:
            return "Number of B_band and V_band must be equal."
        
    else:
        b_v = B_V_band
        logteff = np.zeros(b_v.shape)
        
    
    BC = np.zeros(b_band.shape)
    if stellar_type is None:
        coef = np.array([3.979145106714099,-0.654992268598245,
                         1.740690042385095,-4.608815154057166,
                         6.792599779944473,-5.396909891322525,
                         2.192970376522490,-0.359495739295671])
        for i in range(8):
            logteff += coef[i] *b_v**i
            
    elif stellar_type == "SG":#supergiant
        coef = np.array([4.012559732366214,-1.055043117465989,
                         2.133394538571825,-2.459769794654992,
                         1.349423943497744,-0.283942579112032])
        for i in range(6):
            logteff += coef[i] *b_v**i
            
    teff = 10**(logteff)
    coeff1 = np.array([-0.190537291496456E+05,0.155144866764412E+05,
                       -0.421278819301717E+04,0.381476328422343E+03])
    
    coeff2 = np.array([-0.370510203809015E+05,0.385672629965804E+05,
                       -0.150651486316025E+05,0.261724637119416E+04,
                       -0.170623810323864E+03])
    
    coeff3 = np.array([-0.118115450538963E+06,0.137145973583929E+06,
                       -0.636233812100225E+05,0.147412923562646E+05,
                       -0.170587278406872E+04,0.788731721804990E+02])
    
    index1 = np.where( logteff < 3.70)
    for i in range(4):
        BC[index1] += coeff1[i] *logteff[index1] **i
    
    index2 = np.where( (logteff >=3.70) & (logteff < 3.90))
    for i in range(5):
        BC[index2] += coeff2[i] *logteff[index2] **i
           
    index3 = np.where( logteff >= 3.90)
    for i in range(6):
        BC[index3] += coeff3[i] *logteff[index3] **i

    
    return teff, BC
