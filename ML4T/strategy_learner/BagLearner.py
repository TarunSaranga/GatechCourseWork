
import numpy as np

class BagLearner(object):

    def __init__(self, learner, kwargs={"leaf_size":1}, bags=20, boost=False, verbose = False):
        self.learner = learner
        self.learner_list = []
        self.bags = bags
        np.random.seed(903457046)
        for i in range(0,bags):
            self.learner_list.append(learner(**kwargs))



    def author(self):
        return 'tsaranga3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        idx_list = np.linspace(0,dataX.shape[0]-1,dataX.shape[0])
        idx_list = idx_list.astype(int)

        for learner in self.learner_list:
            idx = np.random.choice(idx_list,idx_list.size)
            learner.addEvidence(dataX.take(idx,axis=0),dataY.take(idx,axis=0))


    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        p = []
        for learner in self.learner_list:
            p.append(learner.query(points))
        p_array = np.array(p)
        ans = np.mean(p_array,axis=0)

        return ans.tolist()


if __name__=="main":
    print("BagLearner Implementation")