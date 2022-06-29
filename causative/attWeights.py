# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 09:40:19 2021

@author: JoeLucas
"""

def attWeights(y,Z,adjType='ATT',fit_intercept=True):
    from sklearn.metrics import roc_curve, auc
    import matplotlib.pyplot as plt
    from pandas.api.types import is_sparse
    from sklearn.linear_model import LogisticRegression

    # y=1*(Z.tier4_id==gg)
    if is_sparse(Z):
        X=Z.sparse.to_coo()
    else:
        X=Z
    
    mod = LogisticRegression(penalty='none',max_iter=1000,fit_intercept=fit_intercept).fit(X, y)
    
    yhat=mod.predict_proba(X)[:,1]
        
    fpr, tpr, _ = roc_curve(y,yhat)
    if adjType=='ATT':
        w=np.where(y==0,yhat/(1-yhat),1)
    elif adjType=='overlap':
        w=np.where(y==0,yhat,1-yhat)
    elif adjType=='ATE':
        w=np.where(y==0,1/(1-yhat),1/yhat)
    # print(pd.DataFrame(zip(list(X),mod.coef_.tolist()[0])))
    print('AUC:',round(auc(fpr, tpr),3))
    print('Max weight:',round(max(w[y==0]),3))
    print('Population size:',sum(y))
    print('Effective comparator size:',round(sum(w[y==0])))
    
    return((w,auc(fpr, tpr),max(w[y==0])))
    # return(w)
