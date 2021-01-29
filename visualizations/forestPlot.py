
def forestPlot(ss,att,ylabel=None,ax=None,lbl=None,xlim=None,figsz=(4,10)):
    import pandas as pd
    import matplotlib.pyplot as plt
    import scipy.stats as stats
    clr=(15/256,98/256,160/256)
    d=pd.DataFrame({'alpha':ss,'beta':att-ss,'label':ylabel})
    d['mn']=d.alpha/(d.alpha+d.beta)
    # d.sort_values('mn',inplace=True)
    d.reset_index(inplace=True)
    if not ax: 
        f,ax=plt.subplots(figsize=figsz)
    ax.scatter(d.mn,range(len(d)),color=clr,alpha=.8)
    for i in range(len(d)):
        lw,hi=stats.beta.ppf([.025,.975],d.loc[i,'alpha']+1,d.loc[i,'beta']+1)
        ax.plot([lw,hi],[i,i],color=clr,alpha=.6)
    if lbl: 
        ax.set_title(lbl)
    if ylabel is not None: 
        ax.set_yticks(range(len(d)))
        ax.set_yticklabels(d.label)
    if xlim:
        ax.set_xlim(xlim)
    
