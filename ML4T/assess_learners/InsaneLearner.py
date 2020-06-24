import BagLearner as bl
import LinRegLearner as lrl
import numpy as np                                                                                                                  
                                                                                                                  
class InsaneLearner(object):                                                                                                                  
                                                                                                                  
    def __init__(self, verbose = False):                                                                                                                  
        self.learner_list = []
        for i in range(0,20): 
            self.learner_list.append(bl.BagLearner(lrl.LinRegLearner,kwargs={},bags=20))
                                                                                                                  
    def author(self):                                                                                                                  
        return 'tsaranga3' # replace tb34 with your Georgia Tech username                                                                                                                  
                                                                                                                  
    def addEvidence(self,dataX,dataY):        
        for learner in self.learner_list: 
            learner.addEvidence(dataX,dataY)                                                                                                                                                                                          
                                                                                                         
    def query(self,points):                                                                                                                         
        p = []
        for learner in self.learner_list: 
            p.append(learner.query(points))
            
        return np.mean(np.array(p),axis=0).tolist()
    