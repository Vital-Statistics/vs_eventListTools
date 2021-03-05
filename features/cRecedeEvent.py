# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 07:29:40 2021

@author: JoeLucas
"""

def cRecedeEvent(v,thr,wdw=365.25):
    import math
    import pandas as pd
    import numpy as np
    w= math.exp(math.log(.01)/wdw)
    return( np.power(w,(thr-v.where(v<thr,v,None))/pd.Timedelta(days=1)) )
