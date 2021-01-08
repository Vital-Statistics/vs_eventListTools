# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:26:16 2020

@author: jolucas
"""

def rocTime(dat,lag=0,ctrlLag=0):
    tlag=dat.delta+ctrlLag*(1-dat.device_fails)
    # q=dat.groupby('device').size()
    lst=dat.loc[tlag== -lag,'device'].unique()
    # res=dat.loc[dat.device.isin(q[q>lag].index.values),:]
    return(dat.loc[dat.device.isin(lst) & (tlag== -lag),:])
    
    # return(res.groupby('device').apply(lambda x: x.loc[x.lag==-lag,:]).reset_index(drop=True))
    # return(res.groupby('device').apply(lambda x: x.iloc[-(lag+1),:]).reset_index(drop=True))
    
