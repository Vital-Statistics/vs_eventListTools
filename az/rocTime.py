# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:26:16 2020

@author: jolucas
"""

def rocTime(dat,unitCol,outcomeCol,lag=0,ctrlLag=0):
    tlag=dat.delta+ctrlLag*(1-dat[outcomeCol])
    lst=dat.loc[tlag== -lag,unitCol].unique()
    return(dat.loc[dat[unitCol].isin(lst) & (tlag== -lag),:])
    
    
