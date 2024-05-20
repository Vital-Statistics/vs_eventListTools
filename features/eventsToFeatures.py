#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 11:08:25 2024

@author: rudy
"""

def eventsToFeatures(pts, events, featureCol, featureList=None, lookback=365.25, event_time='event_time', as_of_date='as_of_date', key=['patient_id'], featureType='attenuate'):
    import pandas as pd
    import datetime
    import math
    if type(key)!=list:
        key=[key]
    el=pd.merge(pts[[as_of_date]],events[key+[event_time]+[featureCol]],left_index=True,right_on=key)
    el=el.loc[(el[event_time]<el[as_of_date])]
    if featureType in ['count','binary']:
        el=el.loc[el[event_time]>=el[as_of_date]-datetime.timedelta(days=lookback)]
        el['delta']=1
    else:
        theta=pow(.01,1/lookback)
        el['delta']=(el[as_of_date]-el[event_time]).dt.days.apply(lambda x:pow(theta,x))
    el=el.groupby(key+[featureCol])['delta'].sum().rename('delta')
    if featureType=='binary':
        el=1*(el>0)
    el=el.reset_index()
    ### deal with the possibility that pts has a multi-index
    idx=pts.index.values
    if not all(type(v)==tuple for v in idx):
        idx=[(v,) for v in idx]
    kk=pd.Categorical(list(zip(*[el[col] for col in key])),categories=idx)
    
    if featureList is None:
        featureList=el[featureCol].unique()
    M=v_buildSparse(kk,pd.Categorical(el[featureCol],categories=featureList),delta=el.delta)
    
    M.index=pd.MultiIndex.from_tuples(M.index.values)
    if len(key)==1:
        M.index = M.index.get_level_values(0)
    return(M)
        