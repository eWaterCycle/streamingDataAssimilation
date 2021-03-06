#! /usr/bin/env python
import numpy as np
import math


def EnKF(ensembleForecast, observationEnsemble, transformation):
    #use notation from Evenson 2003.
    
    p = 0.99 # % of Eigenvectors to include in svd method to ensure stability.

    A=ensembleForecast
    D=observationEnsemble
    H=transformation
    N=np.shape(A)[1]

    Apr = A @ (np.eye(N)-(1/N)*np.ones(N))
    Dpr = D - H(A)
    gamma=D @ (np.eye(N)-(1/N)*np.ones(N))


    #now calculate [U,S,V]=SVD(H*Apr+gamma)
    Utemp,Sigma,vH = np.linalg.svd(H(Apr)+gamma)
    #only keep p % of singular values, discard minimum of 1.
    pN = max(1, math.floor(N * (1-p)))

    U=np.zeros([np.shape(D)[0],N])

    U[0:(np.shape(Utemp)[0]),0:min((np.shape(Utemp)[1]-pN-1),np.shape(U)[1]-pN-1)]=Utemp[:,0:min((np.shape(Utemp)[1]-pN-1),np.shape(U)[1]-pN-1)]

    Sigma=np.diag(Sigma) @ np.diag(Sigma).T
    Sigma = np.power(np.diag(Sigma),-1)
    Sigma[-pN:] = 0
    LambdaInv = np.zeros([N,N])
    LambdaInv[0:np.shape(Sigma)[0],0:np.shape(Sigma)[0]]=np.diag(Sigma)

    X1=LambdaInv @ U.T
    X2=X1 @ Dpr
    X3=U @ X2
    X4=H(Apr).T @ X3
    ensembleAnalyses = A + Apr @ X4
    return ensembleAnalyses
