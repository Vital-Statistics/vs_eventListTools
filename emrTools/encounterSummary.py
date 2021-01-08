# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 11:19:12 2018

@author: jel2
"""

def encounterSummary(M,grp=dict()):
    ### add functionality: column identifying presence of group variables
    sTime=M.loc[M.groupby('PAT_ENC_CSN_ID')['EVENT_TIME'].idxmin(),['PAT_ID','EVENT_TIME','PAT_ENC_CSN_ID']].rename(columns={'EVENT_TIME':'eStartTime'})
    sTime=sTime.join(M.groupby('PAT_ENC_CSN_ID')['EVENT_TIME'].max().rename('eEndTime'),on='PAT_ENC_CSN_ID')
    
    return(sTime)
