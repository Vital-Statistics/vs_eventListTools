#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:47:03 2020

@author: diego
"""

def az_features(df,cols,nLookback=5):
    n=df.shape[0]
    M=None
    for i in range(nLookback):
        M=pd.concat(M,df[range(i,n-nLookback+i),cols],axis=0)
        
        
