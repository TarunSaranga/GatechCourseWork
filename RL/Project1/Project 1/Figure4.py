import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA

def GenerateRandomWalkSequence(NodesCount = 7):
    pos = int((NodesCount - 1)/2)
    
    r = [pos]
    while(1):
        if(random.random() > 0.5):
            nextwalk = 1
        else:
            nextwalk = -1
        
        pos = pos + nextwalk
        if(pos == NodesCount-1):
            z = 1
            break
        elif(pos == 0):
            z = 0
            break
        else:
            r = r + [pos]

    return r , z


def VectorRMS(x):
    rms = LA.norm(x)
    rms = rms/(np.sqrt(5))
    
    return rms

def TDLambda(NodesCount, seq, z, w0, alpha, lambda1):
    w = w0
    w2 = w.copy()
    xt = GetObservationVector(NodesCount, seq[0])
    Pt = np.matmul(np.transpose(w),xt)
    S = xt.copy()
    for i in range(1,len(seq)):
        xt = GetObservationVector(NodesCount, seq[i])
        Pt_1 = Pt.copy()
        Pt = np.matmul(np.transpose(w),xt)
        dw = alpha * (Pt - Pt_1)*S
        S = xt + (lambda1 * S)
        w2 = w2 + dw
    
    dw = alpha * (z - Pt)*S
    w2 = w2 + dw
    w = w2
    
    return w

def GetObservationVector(NodesCount,i):
    xt = np.zeros((NodesCount,1))
    xt[i] = 1
    
    return xt

def PredictionRandomWalk():
    alphas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    nStates = 7
    nTrainingSets = 100
    nSequences = 5
    lambdas = [0,0.35,0.8,1]
    
    optValues = np.arange(1,(nStates - 1))/(nStates - 1)
    totalRMS  = np.zeros((len(alphas),1))
    plt.figure()
    for li in range(len(lambdas)):
        totalRMS  = np.zeros((len(alphas),1))
        for ti in range(nTrainingSets):
            trainingSet = []
        
            for si in range(nSequences):
                [r,z] = GenerateRandomWalkSequence(NodesCount=nStates)
                trainingSet.append([r,z])
        
            for ai in range(len(alphas)):
                w = 0.5 * np.ones((nStates,1))
                w[ 0] = 0 
                w[-1] = 1
                for si in range(nSequences):
                    curSeq = trainingSet[si]
                    z = curSeq[1]
                    curSeq = curSeq[0]
                    w = TDLambda(nStates, curSeq, z, w, alphas[ai], lambdas[li])
                rmsErr = VectorRMS(np.transpose(w[1:nStates-1]) - optValues)
                totalRMS[ai] = totalRMS[ai] + rmsErr
    
        totalRMS = totalRMS / nTrainingSets
    
    
        plt.plot(alphas, totalRMS,'.-', label = str(lambdas[li]))

    plt.legend()
    plt.xlabel('Alpha')
    plt.ylabel('RMS Error')
    plt.ylim((0,0.7))
    plt.show()
    
    return totalRMS

PredictionRandomWalk()
