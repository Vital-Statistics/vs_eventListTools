#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:17:12 2020

@author: diego
"""

def azPlotMetric(dat,nm,timeCol='delta',rt=0,ciMean=True):
    import pandas as pd
    import matplotlib.pyplot as plt

    M=dat.groupby([timeCol,'device_fails']).apply(lambda x: pd.Series({
        'mn': x[nm].mean(), 
        'sd': x[nm].std(),
        'N': x.shape[0],
        'q_low': x[nm].quantile(.25),
        'q_hi': x[nm].quantile(.75)
        })).reset_index()
    if ciMean:
        M['low']=M.mn-1.96*M.sd/(M.N**(1/2))
        M['hi']=M.mn+1.96*M.sd/(M.N**(1/2))
    else:
        M['low']=M.mn-1.96*M.sd
        M['hi']=M.mn+1.96*M.sd
    Q=M.loc[M.device_fails==0,:]
    plt.fill_between(Q[timeCol],Q.low,Q.hi,color=(0,0,.3,.3))
    plt.plot(Q[timeCol],Q.mn,color=(0,0,1,1),label='No Falures')
    plt.xticks(rotation=rt)
    plt.xlabel('Time (Days)')
    plt.ylabel('Average Risk')
    
    Q=M.loc[M.device_fails==1,:]
    plt.fill_between(Q[timeCol],Q.low,Q.hi,color=(1,0,0,.3))
    plt.plot(Q[timeCol],Q.mn,color=(1,0,0,1),label='Failure')
    plt.legend(loc='upper left')
    return(M)
