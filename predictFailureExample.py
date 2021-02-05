#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 22:34:08 2020

@author: diego
"""

import os
import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import keras
import seaborn as sns
import math
import sklearn.linear_model as lm
from sklearn.model_selection import train_test_split
from sklearn import metrics
import xgboost as xgb
import itertools

pd.set_option('display.max_columns', None)

# os.chdir(<path to scripts)

#### Read the helper scripts from the az subfolder
for fl in glob('az/*.py'):
    exec(open(fl).read(),globals())

D=pd.read_csv('data/failureData.csv')

#### All of the models to test.  This could be a lot bigger
cc=list(zip(*list(itertools.product([False,True],[0,25,50],[0,7,14]))))
conditions=pd.DataFrame({'timeFilter':cc[0],'wdw':cc[1],'trainLag':cc[2],'regression':0,'xgboost':0})
cols=['m'+str(i) for i in range(1,7)]
for rowNum,rw in conditions.iterrows():
    print(rowNum,'of',len(conditions),'\n')

    dat=D.copy()
    ### modify features for each variable
    for nm in cols:
        dat[nm]=dat.groupby('Device ID')[nm].transform(lambda x: azFeature(x,signalWindow=rw.loc['wdw']))

    if rw.loc['timeFilter']:
        ctrlLag=20
    else:
        ctrlLag=0
    S=rocTime(dat,'Device ID','Failure',lag=rw.loc['trainLag'],ctrlLag=ctrlLag)
    
    #### Regression
    mod_reg=lm.LogisticRegression(max_iter=500)
    S=S.join(xval_train(mod_reg,S,cols,'Device ID','Failure').rename('regression'),on='Device ID')
    fpr, tpr, _ = metrics.roc_curve(S.Failure,S.regression)
    conditions.loc[rowNum,'regression']=metrics.auc(fpr,tpr)
    

    #### XGBoost
    dat['yhat']=0
    mod_xgb=xgb.XGBClassifier(objective='binary:logistic', colsample_bytree = 0.3, max_depth=3, learning_rate = 0.1, alpha = 1, n_estimators = 10)
    S=S.join(xval_train(mod_xgb,S,cols,'Device ID','Failure',dat=dat).rename('xgboost'),on='Device ID')
    fpr, tpr, _ = metrics.roc_curve(S.Failure,S.xgboost)
    conditions.loc[rowNum,'xgboost']=metrics.auc(fpr,tpr)
    
    _=azPlotMetric(dat.loc[dat.delta>-100,:],'yhat','Failure')
    plt.show()
    
    if rowNum==0:
        at=azAucTrace(dat,'Device ID','Failure').rename(columns={'auc':'auc_condition0'})
    else:
        at=at.join(azAucTrace(dat,'Device ID','Failure')[['delta','auc']].set_index('delta')['auc'].rename('auc_condition'+str(rowNum)),on='delta')

#### Coalate the results
RR=conditions.copy()
RR['delta0']=0
RR['delta14']=0
for i,nm in enumerate(['auc_condition'+str(i) for i in range(len(conditions))]):
    RR.loc[i,'delta0']=float(at.loc[at.delta==0,nm])
    RR.loc[i,'delta14']=float(at.loc[at.delta==-14,nm])

#### Plot AUC for each model through time
for nm in ['auc_condition'+str(i) for i in range(len(conditions))]:
    plt.plot(-at.delta,at[nm])

