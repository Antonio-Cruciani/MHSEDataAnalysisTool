import  math as mt
#from rpy2.robjects.packages import importr
#from rpy2.robjects.vectors import StrVector
import rpy2.robjects as ro
from scipy import stats

class summary:

    def __init__(self,algo,direction,seed):
        self.algorithm = algo
        self.messageDirection = direction
        self.seedNumber = seed
        self.avgDistance = None
        self.effectiveDiameter = None
        self.lowerBoundDiameter = None
        self.totalCouples = None
        self.maxMemoryUsed = None

        # Mean Values

        self.avgDistanceSampleMean = None
        self.effectiveDiameterSampleMean = None
        self.lowerBoundDiameterSampleMean = None
        self.totalCouplesSampleMean = None
        self.maxMemoryUsedSampleMean = None

        # Standard Deviation

        self.avgDistanceSampleStd = None
        self.effectiveDiameterSampleStd = None
        self.lowerBoundDiameterSampleStd = None
        self.totalCouplesSampleStd = None
        self.maxMemoryUsedSampleStd = None

        # Ground Truth

        self.avgDistanceGT = None
        self.effectiveDiameterGT = None
        self.lowerBoundDiameterGT = None
        self.totalCouplesGT = None

        # Residual

        self.avgDistanceResidual = None
        self.effectiveDiameterResidual = None
        self.lowerBoundDiameterResidual = None
        self.totalCouplesResidual = None

        # T-test values
        self.TtestAlpha = None
        # List of two elements: [t-statistic, Two sided p-value]
        self.TtestAvgDistanceAndAvgDistanceGT = None
        self.TtestEffectiveDiameterAndEffectiveDiameterGT = None
        self.TtestLowerBoundDiameterANDLowerBoundDiameterGT = None
        self.TtestTotalCouplesAndTotalCouplesGT = None

    def SampleMeans(self,avg_distance_list= [],effective_diameter_list= [],lowerbound_diamter_list= [],total_coumples_list= [],max_memory_used_list = []):

        if(avg_distance_list):
            self.avgDistance = avg_distance_list
            self.avgDistanceSampleMean = sum(avg_distance_list)/len(avg_distance_list)

        if(effective_diameter_list):
            self.effectiveDiameter = effective_diameter_list
            self.effectiveDiameterSampleMean = sum(effective_diameter_list)/len(effective_diameter_list)

        if(lowerbound_diamter_list):
            self.lowerBoundDiameter = lowerbound_diamter_list
            self.lowerBoundDiameterSampleMean = sum(lowerbound_diamter_list)/len(lowerbound_diamter_list)

        if(total_coumples_list):
            self.totalCouples = total_coumples_list
            self.totalCouplesSampleMean = sum(total_coumples_list)/len(total_coumples_list)

        if(max_memory_used_list):
            self.maxMemoryUsed = max_memory_used_list
            self.maxMemoryUsedSampleMean = sum(max_memory_used_list)/len(max_memory_used_list)

    def StandardDeviations(self):
        if((self.avgDistanceSampleMean == None) and (self.effectiveDiameterSampleMean == None) and (self.lowerBoundDiameterSampleMean == None) and (self.total_coumples_list == None) and (self.maxMemoryUsedSampleMean == None)):
            print("Error! You must calculate sample means first!")
            exit(-1)
        if(self.avgDistanceSampleMean != None):

            self.avgDistanceSampleStd = 0
            for elem in self.avgDistance:
                self.avgDistanceSampleStd +=mt.pow(elem - self.avgDistanceSampleMean ,2)
            self.avgDistanceSampleStd = self.avgDistanceSampleStd/len(self.avgDistance)
            self.avgDistanceSampleStd = mt.sqrt(self.avgDistanceSampleStd)

        if(self.effectiveDiameterSampleMean != None):

            self.effectiveDiameterSampleStd = 0
            for elem in self.effectiveDiameter:
                self.effectiveDiameterSampleStd += mt.pow(elem - self.effectiveDiameterSampleMean, 2)
            self.effectiveDiameterSampleStd = self.effectiveDiameterSampleStd / len(self.effectiveDiameter)
            self.effectiveDiameterSampleStd = mt.sqrt(self.effectiveDiameterSampleStd)

        if(self.lowerBoundDiameterSampleMean != None):

            self.lowerBoundDiameterSampleStd = 0
            for elem in self.lowerBoundDiameter:
                self.lowerBoundDiameterSampleStd += mt.pow(elem - self.lowerBoundDiameterSampleMean, 2)
            self.lowerBoundDiameterSampleStd = self.lowerBoundDiameterSampleStd / len(self.lowerBoundDiameter)
            self.lowerBoundDiameterSampleStd = mt.sqrt(self.lowerBoundDiameterSampleStd)

        if(self.totalCouplesSampleMean != None):
            self.totalCouplesSampleStd = 0
            for elem in self.totalCouples:
                self.totalCouplesSampleStd += mt.pow(elem - self.totalCouplesSampleMean, 2)
            self.totalCouplesSampleStd = self.totalCouplesSampleStd / len(self.totalCouples)
            self.totalCouplesSampleStd = mt.sqrt(self.totalCouplesSampleStd)


        if(self.maxMemoryUsedSampleMean != None):

            self.maxMemoryUsedStd = 0
            for elem in self.maxMemoryUsed:
                self.maxMemoryUsedStd += mt.pow(elem - self.maxMemoryUsedSampleMean, 2)
            self.maxMemoryUsedStd = self.maxMemoryUsedStd / len(self.maxMemoryUsed)
            self.maxMemoryUsedSampleStd = mt.sqrt(self.maxMemoryUsedStd)


    def Residuals(self):

        if ((self.avgDistanceSampleMean == None) and (self.effectiveDiameterSampleMean == None) and (
                self.lowerBoundDiameterSampleMean == None) and (self.total_coumples_list == None) and (
                self.maxMemoryUsedSampleMean == None)):
            print("Error! You must calculate sample means first!")
            exit(-1)

        if ((self.avgDistanceGT == None) and (self.effectiveDiameterGT == None) and (
                self.lowerBoundDiameterGT == None) and (self.totalCouplesGT == None)):
            print("Error! You must set ground truth values first!")
            exit(-1)

        self.avgDistanceResidual  = ((self.avgDistanceSampleMean - self.avgDistanceGT) / self.avgDistanceGT)*100
        self.effectiveDiameterResidual = ((self.effectiveDiameterSampleMean - self.effectiveDiameterGT )/ self.effectiveDiameterGT)*100
        self.lowerBoundDiameterResidual = ((self.lowerBoundDiameterSampleMean - self.lowerBoundDiameterGT) / self.lowerBoundDiameterGT)*100
        self.totalCouplesResidual = ((self.totalCouplesSampleMean - self.totalCouplesGT) / self.totalCouplesGT)*100

    # Calculate the T - test for the mean of ONE group of scores.
    # This is a two - sided test for the null hypothesis that the expected value (mean) of a sample of independent observations a
    # is equal to the given population mean

    def Ttest(self):

        if ((self.avgDistanceSampleMean == None) and (self.effectiveDiameterSampleMean == None) and (
                self.lowerBoundDiameterSampleMean == None) and (self.total_coumples_list == None) and (
                self.maxMemoryUsedSampleMean == None)):
            print("Error! You must calculate sample means first!")
            exit(-1)

        if ((self.avgDistanceGT == None) and (self.effectiveDiameterGT == None) and (
                self.lowerBoundDiameterGT == None) and (self.totalCouplesGT == None)):
            print("Error! You must set ground truth values first!")
            exit(-1)

        # 1. Pass data from Python into R
        xAvgDistance = ro.vectors.FloatVector(self.avgDistance)
        xEffectiveDiameter = ro.vectors.FloatVector(self.effectiveDiameter)
        xLowerBoundDiameter = ro.vectors.FloatVector(self.lowerBoundDiameter)
        xTotalCouples = ro.vectors.FloatVector(self.totalCouples)
        # 2. Call t.test on data in R
        ttest = ro.r['t.test']

        #res = ttest(xr, yr,paired=False, alternative = "two.sided",conflevel = 0.95)
        resAvgDistance = ttest(xAvgDistance,mu=self.avgDistanceGT, paired=False, alternative="two.sided", conflevel=0.95)
        resEffectiveDiameter = ttest(xEffectiveDiameter, mu=self.effectiveDiameterGT, paired=False, alternative="two.sided",
                              conflevel=0.95)
        resLowerBoundDiameter = ttest(xLowerBoundDiameter, mu=self.lowerBoundDiameterGT, paired=False, alternative="two.sided",
                              conflevel=0.95)


        resTotalCouples =  ttest(xTotalCouples, mu=float(self.totalCouplesGT), paired=False, alternative="two.sided",
                              conflevel=0.95)
        # print("RISULTATO T TEST avgDist",resAvgDistance)
        # print("RISULTATO T TEST effDiam", resEffectiveDiameter)
        # print("RISULTATO T TEST lowD", resLowerBoundDiameter)
        # print("RISULTATO T TEST TotalC", resTotalCouples)
        # 3. Pass data from R back into Python


        self.TtestAvgDistanceAndAvgDistanceGT = resAvgDistance.rx2('p.value')[0]
        self.TtestEffectiveDiameterAndEffectiveDiameterGT = resEffectiveDiameter.rx2('p.value')[0]
        self.TtestLowerBoundDiameterANDLowerBoundDiameterGT = resLowerBoundDiameter.rx2('p.value')[0]
        self.TtestTotalCouplesAndTotalCouplesGT = resTotalCouples.rx2('p.value')[0]
        print(self.TtestAvgDistanceAndAvgDistanceGT )
        #st.t_test(self.avgDistance,self.avgDistanceGT,**{'var.equal': False,
        #                                                         'paired': False,''
        #                                                 'alternative':StrVector(("two.sided",))
        #                                                 })

        #self.TtestAvgDistanceAndAvgDistanceGT = stats.ttest_1samp(self.avgDistance,self.avgDistanceGT)

        # self.TtestEffectiveDiameterAndEffectiveDiameterGT = stats.ttest_1samp(self.effectiveDiameter,self.effectiveDiameterGT)
        # self.TtestLowerBoundDiameterANDLowerBoundDiameterGT = stats.ttest_1samp(self.lowerBoundDiameter,self.lowerBoundDiameterGT)
        # self.TtestTotalCouplesAndTotalCouplesGT = stats.ttest_1samp(self.totalCouples,self.totalCouplesGT)




    # ground_truth mus have the following structure:
    #{
     #   "avgDistance": value,
     #   "effectiveDiameter": value,
     #   "lowerBoundDiameter": value,
     #   "totalCouples": value
    #}

    def set_all_ground_truth(self,ground_truth):

        self.avgDistanceGT = ground_truth['avgDistance']
        self.effectiveDiameterGT = ground_truth['effectiveDiameter']
        self.lowerBoundDiameterGT = ground_truth['lowerBoundDiameter']
        self.totalCouplesGT = ground_truth['totalCouples']

    def set_avgDistanceGT(self,GT):
        self.avgDistanceGT = GT

    def set_effectiveDiameterGT(self,GT):
        self.effectiveDiameterGT = GT

    def set_lowerBoundDiameterGT(self, GT):
        self.lowerBoundDiameterGT = GT

    def set_totalCouplesGT(self, GT):
        self.totalCouplesGT = GT

    def get_algorithm(self):
        return(self.algorithm)

    def get_messageDirection(self):

        return(self.messageDirection)
    def get_seedNumber(self):
        return(self.seedNumber)

    def get_avgDistance(self):
        return(self.avgDistance)

    def get_effectiveDiameter(self):
        return(self.effectiveDiameter)

    def get_lowerBoundDiameter(self):
        return(self.lowerBoundDiameter)

    def get_totalCouples(self):
        return(self.totalCouples)

    def get_maxMemoryUsed(self):
        return(self.maxMemoryUsed)

    def get_avgDistanceSampleMean(self):
        return(self.avgDistanceSampleMean)

    def get_effectiveDiameterSampleMean(self):
        return(self.effectiveDiameterSampleMean)

    def get_lowerBoundDiameterSampleMean(self):
        return(self.lowerBoundDiameterSampleMean)

    def get_totalCouplesSampleMean(self):
        return(self.totalCouplesSampleMean)

    def get_maxMemoryUsedSampleMean(self):
        return (self.maxMemoryUsedSampleMean)

    def get_avgDistanceStd(self):
        return(self.avgDistanceSampleStd)

    def get_effectiveDiameterStd(self):
        return(self.effectiveDiameterSampleStd)

    def get_lowerBoundDiameterStd(self):
        return(self.lowerBoundDiameterSampleStd)

    def get_totalCouplesStd(self):
        return(self.totalCouplesSampleStd)

    def get_maxMemoryUsedStd(self):
        return(self.maxMemoryUsedSampleStd)

    def get_avgDistanceResidual(self):
        return(self.avgDistanceResidual)

    def get_effectiveDiameterResidual(self):
        return(self.effectiveDiameterResidual)

    def get_lowerBoundDiameterResidual(self):
        return(self.lowerBoundDiameterResidual)

    def get_totalCouplesResidual(self):
        return(self.totalCouplesResidual)

    def get_TtestAvgDistanceAndAvgDistanceGT(self):
        return(self.TtestAvgDistanceAndAvgDistanceGT)

    def get_TtestEffectiveDiameterAndEffectiveDiameterGT(self):
        return(self.TtestEffectiveDiameterAndEffectiveDiameterGT)

    def get_TtestLowerBoundDiameterANDLowerBoundDiameterGT(self):
        return(self.TtestLowerBoundDiameterANDLowerBoundDiameterGT)

    def get_TtestTotalCouplesAndTotalCouplesGT(self):
        return(self.TtestTotalCouplesAndTotalCouplesGT)

    def get_all_Ttests(self):
        return(
            {
                "avgDistance":self.TtestAvgDistanceAndAvgDistanceGT,
                "effectiveDiameter":self.TtestEffectiveDiameterAndEffectiveDiameterGT,
                "lowerBoundDiameter":self.TtestLowerBoundDiameterANDLowerBoundDiameterGT,
                "totalCouples":self.TtestTotalCouplesAndTotalCouplesGT
            }
        )

