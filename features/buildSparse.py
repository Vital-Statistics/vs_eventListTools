# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:29:12 2017

@author: jel2
"""

def buildSparse(df,a,b,colFilter=None,rowFilter=None,makeBinary=False,rowLabels=None,colLabels=None):
    import scipy
    import pandas as pd
    import numpy as np
    ct=df[[a,b]].groupby([a,b]).size().rename('value').reset_index()
    if rowLabels is not None:
        ct=ct.loc[ct[a].isin(rowLabels)]
        rowLabels=list(rowLabels)
    else:
        rowLabels=list(pd.Series(ct[a].unique()).sort_values())
    if colLabels is not None:
        ct=ct.loc[ct[b].isin(colLabels)]
        colLabels=list(colLabels)
    else:
        colLabels=list(pd.Series(ct[b].unique()).sort_values())
    x=pd.Categorical(ct[a],categories=rowLabels)
    y=pd.Categorical(ct[b],categories=colLabels)
    i=x.codes
    j=y.codes
    rLbl=pd.Series(x.categories)
    cLbl=pd.Series(y.categories)
    if makeBinary: ct.value=1
    M=scipy.sparse.coo_matrix((np.array(ct.value),(i,j)),shape=(len(rLbl),len(cLbl)))
    M=M.tocsr()
    
    if colFilter:
        kp=np.asarray(M.sum(axis=0)).reshape(-1)>=colFilter
        M=M[:,kp]
        cLbl=cLbl.loc[kp]

    if rowFilter:
        kp=np.asarray(M.sum(axis=1)).reshape(-1)>=rowFilter
        M=M[kp,:]
        rLbl=rLbl.loc[kp]
    
    # return([rLbl,cLbl,M])
    return(pd.DataFrame.sparse.from_spmatrix(M,columns=cLbl,index=rLbl))
