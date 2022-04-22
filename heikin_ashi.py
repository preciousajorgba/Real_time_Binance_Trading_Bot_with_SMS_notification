import numpy as np
open=[]
high=[]
low=[]
close=[]
def HEIKIN(O, H, L, C, oldO, oldC):
    HA_Close = (O + H + L + C)/4
    HA_Open = (oldO + oldC)/2
    elements = np.array([H, L, HA_Open, HA_Close])
    HA_High = elements.max() 
    HA_Low = elements.min()

    open.append(round(HA_Open,4))
    high.append(round(HA_High,4))
    low.append(round(HA_Low,4))
    close.append(round(HA_Close,4))
    return open,high,low,close

    

