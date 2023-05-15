import settings

class GlobalStats:
    Means = []
    Variances = []
    Skewness = []
    Kurtosis = []

    def __init__(self):
        self.n = settings.n
        self.Means = []
        self.Variances = []
        self.Skewness = []
        self.Kurtosis = []

    def makeNewStats(self, corr):
        m = self.findMeanCoef(corr)
        v = self.findVariance(corr, m)
        s = self.findSkewness(corr, m, v)
        k = self.findKurtosis(corr, m, v)

        self.Means.append(m)
        self.Variances.append(v)
        self.Skewness.append(s)
        self.Kurtosis.append(k)
        return [m, v, s, k]

    def getAllStats(self):
        return [self.Means, self.Variances, self.Skewness, self.Kurtosis]

    def findMeanCoef(self, corr):
        s = self.__calculateCoefMatrixSum(corr, 0, 1)
        return (2*s)/(self.n*(self.n - 1))

    def findVariance(self, corr, m):
        s = self.__calculateCoefMatrixSum(corr, m, 2, 1)
        return (2*s)/(self.n*(self.n - 1))

    def findSkewness(self, corr, m, v):
        s = self.__calculateCoefMatrixSum(corr, m, 3, pow(v, 1.5))
        return (2*s)/(self.n*(self.n - 1))

    def findKurtosis(self, corr, m, v):
        s = self.__calculateCoefMatrixSum(corr, m, 4, pow(v, 2)) 
        return (2*s)/(self.n*(self.n - 1))
    
    def __calculateCoefMatrixSum(self, corr, m, power, divisor=1):
        s = 0
        for i in range(self.n):
            for j in range(i):
                s += (((corr[i][j] - m)**power) / divisor)
        
        return s