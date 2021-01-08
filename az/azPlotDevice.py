# -*- coding: utf-8 -*-
"""
Created on Tue May 26 09:47:28 2020

@author: jolucas
"""

def azPlotDevice(dat,mrc,dList):
    import matplotlib.pyplot as plt
    #### plot each device separately
    for nm in dList:
        df=dat.loc[dat.device==nm,:]
        plt.plot(df.date,df[mrc])
    plt.show()
