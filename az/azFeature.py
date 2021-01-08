# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:28:28 2020

@author: jolucas
"""

def azFeature(x,signalWindow=25):
    import math
    import pandas as pd
    base=[0]
    if signalWindow==0:
        q=1
    else:
        q=math.exp(math.log(.001)/signalWindow)
    for i in range(len(x)):
        base=base+[base[-1]*q+x.iloc[i]]
    return(pd.array(base[1:]))

