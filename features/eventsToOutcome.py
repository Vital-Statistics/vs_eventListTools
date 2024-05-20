#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 10:41:22 2024

@author: rudy
"""

def eventsToOutcome(pts,events,outcomeWindow=180, event_time='event_time', as_of_date='as_of_date', counts=False, key=['patient_id']):
    import pandas as pd
    import datetime
    if type(key)!=list:
        key=[key]
    el=pd.merge(pts[[as_of_date]],events[key+[event_time]],left_index=True,right_on=key)
    el=el.loc[(el[event_time]>=el[as_of_date]) & (el[event_time]<el[as_of_date]+datetime.timedelta(days=outcomeWindow))]
    el=el.groupby(key).size()
    res=pts[[]].join(el.rename('y')).fillna(0)
    if not counts:
        res=1*(res>0)
    return(res)