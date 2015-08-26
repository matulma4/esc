#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:17:03 2015

@author: silvicek
"""

from basicgrad import getInputs,mrrcount,mrr,testGrad,setRes
import numpy as np
import pickle
from sklearn import linear_model
MATRIX_SIZE = 2
def trecEval(li):
    truth=open('truth.txt','w')
    res=open('res.txt','w')
    for i in range(0,len(li)):
        for j in range(0,len(li[i].y)):
            truth.write(' '.join(map(str,(i,0,j,int(li[i].y[j]),'\n'))))
            res.write(' '.join(map(str,(i,0,j,1,li[i].tcount[j],'glove','\n'))))
    truth.close()
    res.close()
    print 'trec_eval created'
    return
    

def train(trainlist,testlist):
    """Unigram+word count training from saved Qlist files, returns weights, generates trec_eval documents"""
    # (trainlist,ans1,ans0)=loadList(LISTPATH,PANS1,PANS0)
    # (testlist,tans1,tans0)=loadList(TLISTPATH,PTANS1,PTANS0)
    print 'data loaded'

    M=np.random.normal(0,0.01,(MATRIX_SIZE,MATRIX_SIZE))
    b=-0.0001
    (M,b)=testGrad(M,b,trainlist)
    # M=np.loadtxt('data/M77.txt')
    # b=np.loadtxt('data/b77.txt')

    print 'MRR after unigram learning:',mrr(M,b,testlist)

    pickle.dump((M, b), open("unigram-Mb.pickle", "wb"))
    print 'pickled unigram-Mb.pickle'

    # XXX: This has a sideeffect, setting resolutions in trainlist
#     mrr(M,b,trainlist)
#
#     (x,y)=getInputs(trainlist,ans1,ans0)
#     (xtest,ytest)=getInputs(testlist,tans1,tans0)
#     clf = linear_model.LogisticRegression(C=100, penalty='l2', tol=1e-5,solver='lbfgs')
#     clf.fit(x, y)
#     tcounttest=clf.predict_proba(xtest)
#     setRes(testlist,tans1,tans0,tcounttest[:,1])
#     print 'MRR unigram+count',mrrcount(testlist,tans1,tans0)
#
#     trecEval(testlist)
#     w=clf.coef_
#     w=np.append(w,clf.intercept_);
# #    print w
#     np.savetxt('data/weights.txt',w)
    return (M, b)


if __name__ == "__main__":
    # Seed always to the same number to get reproducible models
    np.random.seed(17151713)

    (M, b) = train([],[])# train(LISTPATH, PANS1, PANS0, TLISTPATH, PTANS1, PTANS0)
    print M
    print b
