import json
import pandas as pd
#import numpy as np
import sys, getopt
import rpy2.robjects as ro
from objects.scores import summary
#from objects.stats import resultsStats




def read_json(InputPath,OutputPath,GroundTruthPath = None,std = True,Ttest = False,dataframe = False,LabelPath = None,rounding = 5):

    experiments = {}
    statistics = {}
    results = {}
    # provvisorio
    #sample_residuals = {}
    groundTruth = {}
    if((Ttest == True ) and GroundTruthPath == None ):
        print("Error! If you want to perform a Ttest between samples and groundtruth you need also the groundtruth values")
        exit(-1)
    try:
        with open(InputPath) as json_file:
            data = json.load(json_file)
    except IOError:
        print('Error! Can not open '+InputPath)

    if(GroundTruthPath != None):
        try:
            with open(GroundTruthPath) as json_gt:
                groundTruth = json.load(json_gt)
        except IOError:
            print('Error! Can not open ' + json_gt)

    seed_list = []
    algo_list = []
    in_direction = False
    out_direction = False
    direction_list = []
    for elem in data:
        if not(elem['num_seeds'] in seed_list):
            seed_list.append(elem['num_seeds'])
        if not(elem['algorithm'] in algo_list):
            algo_list.append(elem['algorithm'])
        if(elem['direction'] == 'out'):
            out_direction = True
        elif(elem['direction'] == 'in'):
            in_direction = True


    if(out_direction):
        direction_list.append("out")
    if(in_direction):
        direction_list.append("in")

    # Building a dictionary entry for each type of simulation

    for algo in algo_list:

        for direction in direction_list:
            for seed in seed_list:

                experiments[(algo,direction,seed,"avg_distance")] =[]
                experiments[(algo,direction,seed,"effective_diameter")] = []
                experiments[(algo,direction,seed,"diameter")] = []
                experiments[(algo,direction,seed,"total_couples")] = []
                experiments[(algo,direction,seed,"memory_used")] = []


    for elem in data:


        experiments[(elem['algorithm'],elem['direction'],elem['num_seeds'],"avg_distance")].append(elem['avg_distance'])
        experiments[(elem['algorithm'],elem['direction'],elem['num_seeds'],"effective_diameter")].append(elem['effective_diameter'])
        experiments[(elem['algorithm'],elem['direction'],elem['num_seeds'],"diameter")].append(elem['diameter'])
        experiments[(elem['algorithm'],elem['direction'],elem['num_seeds'],"total_couples")].append(elem['total_couples'])
        experiments[(elem['algorithm'],elem['direction'],elem['num_seeds'],"memory_used")].append(elem['memory_used'])


    # Building a dictionary for the statistics

    for algo in algo_list:
        for direction in direction_list:
            for seed in seed_list:

                statistics[(algo,direction,seed)] = summary(algo,direction,seed)


                statistics[(algo,direction,seed)].SampleMeans(experiments[(algo,direction,seed,"avg_distance")],experiments[(algo,direction,seed,"effective_diameter")],
                                                            experiments[(algo,direction,seed,"diameter")],
                                                            experiments[(algo,direction,seed,"total_couples")],experiments[(algo,direction,seed,"memory_used")]
                                                            )

                results[(algo,direction,seed,"MeanAvgDistance")] = [statistics[(algo,direction,seed)].get_avgDistanceSampleMean()]
                results[(algo,direction,seed,"MeanEffectiveDiameter")] = [statistics[(algo,direction,seed)].get_effectiveDiameterSampleMean()]
                results[(algo,direction,seed,"MeanLowerBoundDiameter")] = [statistics[(algo,direction,seed)].get_lowerBoundDiameterSampleMean()]
                results[(algo,direction,seed,"MeanTotalCouples")] = [statistics[(algo,direction,seed)].get_totalCouplesSampleMean()]
                results[(algo,direction,seed,"MeanMaxMemoryUsed")] = [statistics[(algo,direction,seed)].get_maxMemoryUsedSampleMean()]


                if(std):

                    statistics[(algo,direction,seed)].StandardDeviations()

                    results[(algo, direction, seed, "MeanAvgDistance")].append(
                        statistics[(algo, direction, seed)].get_avgDistanceStd())
                    results[(algo, direction, seed, "MeanEffectiveDiameter")].append(
                        statistics[(algo, direction, seed)].get_effectiveDiameterStd())
                    results[(algo, direction, seed, "MeanLowerBoundDiameter")].append(
                        statistics[(algo, direction, seed)].get_lowerBoundDiameterStd())
                    results[(algo, direction, seed, "MeanTotalCouples")].append(
                        statistics[(algo, direction, seed)].get_totalCouplesStd())

                    results[(algo, direction, seed, "MeanMaxMemoryUsed")].append(
                        statistics[(algo, direction, seed)].get_maxMemoryUsedStd())

                if(GroundTruthPath != None):
                    statistics[(algo, direction, seed)].set_all_ground_truth(groundTruth)
                    statistics[(algo, direction, seed)].Residuals()
                    residuals = {}

                    residuals['avg_distance'] = statistics[(algo, direction, seed)].get_avgDistanceResidual()
                    residuals['effective_diameter'] = statistics[(algo, direction, seed)].get_effectiveDiameterResidual()
                    residuals['diameter'] = statistics[
                        (algo, direction, seed)].get_lowerBoundDiameterResidual()
                    residuals["total_couples"] = statistics[(algo, direction, seed)].get_totalCouplesResidual()
                    results[(algo, direction, seed, "residuals")] = residuals

                    CI = {}

                    CI['avg_distance'] = statistics[(algo, direction, seed)].get_ciAvgDistance()
                    CI['effective_diameter'] = statistics[(algo, direction, seed)].get_ciEffectiveDiameter()
                    CI['diameter'] = statistics[(algo, direction, seed)].get_ciLowerBoundDiameter()
                    CI['total_couples'] = statistics[(algo, direction, seed)].get_ciTotalCouples()
                    results[(algo, direction, seed, "confidence_Interval")] = CI

                    # sample_residuals[(algo,direction,seed,"avg_distance")] = statistics[(algo, direction, seed)].get_avgDistanceResidualSample()
                    # sample_residuals[(algo, direction, seed, "effective_diameter")] = statistics[
                    #     (algo, direction, seed)].get_effectiveDiameterResidualSample()
                    # sample_residuals[(algo, direction, seed, "diameter")] = statistics[
                    #     (algo, direction, seed)].get_lowerBoundDiameterResidualSample()
                    # sample_residuals[(algo, direction, seed, "total_couples")] = statistics[
                    #     (algo, direction, seed)].get_totalCouplesResidualSample()

                if(Ttest):
                    statistics[(algo, direction, seed)].Ttest()
                    results[(algo, direction, seed, "Ttest")] = statistics[(algo, direction, seed)].get_all_Ttests()

                # print(algo, direction, seed)
                # print("Sample Mean AVG DISTANCE = ", results[(algo, direction, seed, "MeanAvgDistance")])
                # print("Sample Mean E DIAMETER = ", results[(algo, direction, seed, "MeanEffectiveDiameter")])
                # print("Sample Mean LB DIAMETER = ", results[(algo, direction, seed, "MeanLowerBoundDiameter")])
                # print("Sample Mean total couples  = ", results[(algo, direction, seed, "MeanTotalCouples")])
                # print("Sample Mean MeanMaxMemoryUsed  = ", results[(algo, direction, seed, "MeanMaxMemoryUsed")])
    #writableJson = dict((':'.join(k), v) for k, v in results.items())

    if(dataframe):
        head = ["algo","direction","seeds"]
        if(std):
            if(GroundTruthPath):
                if(Ttest):
                    head.extend(["groundTruthAvgDistance","sampleMeanAvgDistance","stdAvgDistance","residualAvgDistance","pValueAvgDistance","ciAvgDistance",
                "groundTruthEffectiveDiameter","sampleMeanEffectiveDiameter","stdEffectiveDiameter","residualEffectiveDiameter","pValueEffectiveDiameter","ciEffectiveDiameter",
                "groundTruthLowerBoundDiameter","sampleMeanLowerBoundDiameter","stdLowerBoundDiameter","residualLowerBoundDiameter","pValueLowerBoundDiameter","ciLowerBoundDiameter",
                "groundTruthTotalCouples","sampleMeanTotalCouples","stdTotalCouples","residualTotalCouples","pValueTotalCouples","CITotalCouples"])
                    elements = []
                    for algo in algo_list:
                        for direction in direction_list:
                            for seed in seed_list:
                                elements.append([
                                    algo, direction, seed, groundTruth['avg_distance'],
                                    results[(algo, direction, seed, "MeanAvgDistance")][0],
                                    results[(algo, direction, seed, "MeanAvgDistance")][1],
                                    results[(algo, direction, seed, "residuals")]["avg_distance"],
                                    results[(algo, direction, seed, "Ttest")]['avg_distance'],
                                    results[(algo, direction, seed, "confidence_Interval")]['avg_distance'],

                                    groundTruth['effective_diameter'],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][1],
                                    results[(algo, direction, seed, "residuals")]["effective_diameter"],
                                    results[(algo, direction, seed, "Ttest")]['effective_diameter'],
                                    results[(algo, direction, seed, "confidence_Interval")]['effective_diameter'],

                                    groundTruth['diameter'],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][1],
                                    results[(algo, direction, seed, "residuals")]["diameter"],
                                    results[(algo, direction, seed, "Ttest")]['diameter'],
                                    results[(algo, direction, seed, "confidence_Interval")]['diameter'],

                                    groundTruth['total_couples'],
                                    results[(algo, direction, seed, "MeanTotalCouples")][0],
                                    results[(algo, direction, seed, "MeanTotalCouples")][1],
                                    results[(algo, direction, seed, "residuals")]["total_couples"],
                                    results[(algo, direction, seed, "Ttest")]['total_couples'],
                                    results[(algo, direction, seed, "confidence_Interval")]['total_couples'],


                                ])

                else:
                    head.extend(["groundTruthAvgDistance","sampleMeanAvgDistance","stdAvgDistance","residualAvgDistance",
                "groundTruthEffectiveDiameter","sampleMeanEffectiveDiameter","stdEffectiveDiameter","residualEffectiveDiameter",
                "groundTruthLowerBoundDiameter","sampleMeanLowerBoundDiameter","stdLowerBoundDiameter","residualLowerBoundDiameter",
                "groundTruthTotalCouples","sampleMeanTotalCouples","stdTotalCouples","residualTotalCouples"])
                    elements = []
                    for algo in algo_list:
                        for direction in direction_list:
                            for seed in seed_list:
                                elements.append([
                                    algo, direction, seed, groundTruth['avg_distance'],
                                    results[(algo, direction, seed, "MeanAvgDistance")][0],
                                    results[(algo, direction, seed, "MeanAvgDistance")][1],
                                    results[(algo, direction, seed, "residuals")]["avg_distance"],
                                    groundTruth['effective_diameter'],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][1],
                                    results[(algo, direction, seed, "residuals")]["effective_diameter"],
                                    groundTruth['diameter'],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][1],
                                    results[(algo, direction, seed, "residuals")]["diameter"],
                                    groundTruth['total_couples'],
                                    results[(algo, direction, seed, "MeanTotalCouples")][0],
                                    results[(algo, direction, seed, "MeanTotalCouples")][1],
                                    results[(algo, direction, seed, "residuals")]["total_couples"]
                                ])
            else:
                head.extend([ "sampleMeanAvgDistance", "stdAvgDistance", "residualAvgDistance",
                              "sampleMeanEffectiveDiameter", "stdEffectiveDiameter",
                             "residualEffectiveDiameter",
                             "sampleMeanLowerBoundDiameter", "stdLowerBoundDiameter",
                             "residualLowerBoundDiameter",
                              "sampleMeanTotalCouples", "stdTotalCouples",
                             "residualTotalCouples"])
                elements = []
                for algo in algo_list:
                    for direction in direction_list:
                        for seed in seed_list:
                            elements.append([
                                algo, direction, seed,
                                results[(algo, direction, seed, "MeanAvgDistance")][0],
                                results[(algo, direction, seed, "MeanAvgDistance")][1],
                                results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                results[(algo, direction, seed, "MeanEffectiveDiameter")][1],
                                results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                results[(algo, direction, seed, "MeanLowerBoundDiameter")][1],
                                results[(algo, direction, seed, "MeanTotalCouples")][0],
                                results[(algo, direction, seed, "MeanTotalCouples")][1]
                            ])
        else:
            if (GroundTruthPath):
                if (Ttest):
                    head.extend(
                        ["groundTruthAvgDistance", "sampleMeanAvgDistance", "residualAvgDistance",
                         "pValueAvgDistance",
                         "groundTruthEffectiveDiameter", "sampleMeanEffectiveDiameter",
                         "residualEffectiveDiameter", "pValueEffectiveDiameter",
                         "groundTruthLowerBoundDiameter", "sampleMeanLowerBoundDiameter",
                         "residualLowerBoundDiameter", "pValueLowerBoundDiameter",
                         "groundTruthTotalCouples", "sampleMeanTotalCouples", "residualTotalCouples",
                         "pValueTotalCouples"])
                    elements = []
                    for algo in algo_list:
                        for direction in direction_list:
                            for seed in seed_list:
                                elements.append([
                                    algo, direction, seed, groundTruth['avg_distance'],
                                    results[(algo, direction, seed, "MeanAvgDistance")][0],
                                    results[(algo, direction, seed, "residuals")]["avg_distance"],
                                    results[(algo, direction, seed, "Ttest")]['avg_distance'],
                                    groundTruth['effective_diameter'],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                    results[(algo, direction, seed, "residuals")]["effective_diameter"],
                                    results[(algo, direction, seed, "Ttest")]['effective_diameter'],
                                    groundTruth['diameter'],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                    results[(algo, direction, seed, "residuals")]["diameter"],
                                    results[(algo, direction, seed, "Ttest")]['diameter'],
                                    groundTruth['total_couples'],
                                    results[(algo, direction, seed, "MeanTotalCouples")][0],
                                    results[(algo, direction, seed, "residuals")]["total_couples"],
                                    results[(algo, direction, seed, "Ttest")]['total_couples']

                                ])

                else:
                    head.extend(
                        ["groundTruthAvgDistance", "sampleMeanAvgDistance", "residualAvgDistance",
                         "groundTruthEffectiveDiameter", "sampleMeanEffectiveDiameter",
                         "residualEffectiveDiameter",
                         "groundTruthLowerBoundDiameter", "sampleMeanLowerBoundDiameter",
                         "residualLowerBoundDiameter",
                         "groundTruthTotalCouples", "sampleMeanTotalCouples",
                         "residualTotalCouples"])
                    elements = []
                    for algo in algo_list:
                        for direction in direction_list:
                            for seed in seed_list:
                                elements.append([
                                    algo, direction, seed, groundTruth['avg_distance'],
                                    results[(algo, direction, seed, "MeanAvgDistance")][0],
                                    results[(algo, direction, seed, "residuals")]["avg_distance"],
                                    groundTruth['effective_diameter'],
                                    results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                    results[(algo, direction, seed, "residuals")]["effective_diameter"],
                                    groundTruth['diameter'],
                                    results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                    results[(algo, direction, seed, "residuals")]["diameter"],
                                    groundTruth['total_couples'],
                                    results[(algo, direction, seed, "MeanTotalCouples")][0],
                                    results[(algo, direction, seed, "residuals")]["total_couples"]
                                ])
            else:
                head.extend(["sampleMeanAvgDistance",
                             "sampleMeanEffectiveDiameter",

                             "sampleMeanLowerBoundDiameter",

                             "sampleMeanTotalCouples",
                             ])
                elements = []

                for algo in algo_list:
                    for direction in direction_list:
                        for seed in seed_list:

                            elements.append([
                                algo, direction, seed,
                                results[(algo, direction, seed, "MeanAvgDistance")][0],
                                results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                                results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                                results[(algo, direction, seed, "MeanTotalCouples")][0]

                            ])


        # # Building header
        # head = ["algo","direction","seeds",
        #         "groundTruthAvgDistance","sampleMeanAvgDistance","stdAvgDistance","residualAvgDistance","pValueAvgDistance",
        #         "groundTruthEffectiveDiameter","sampleMeanEffectiveDiameter","stdEffectiveDiameter","residualEffectiveDiameter","pValueEffectiveDiameter",
        #         "groundTruthLowerBoundDiameter","sampleMeanLowerBoundDiameter","stdLowerBoundDiameter","residualLowerBoundDiameter","pValueLowerBoundDiameter",
        #         "groundTruthTotalCouples","sampleMeanTotalCouples","stdTotalCouples","residualTotalCouples","pValueTotalCouples"
        #         ]
        # elements = []
        # for algo in algo_list:
        #     for direction in direction_list:
        #         for seed in seed_list:
        #             if(std and Ttest):
        #                 elements.append([
        #                     algo,direction,seed,groundTruth['avgDistance'],results[(algo, direction, seed,"MeanAvgDistance")][0],results[(algo, direction, seed,"MeanAvgDistance")][1],results[(algo, direction, seed,"residuals")]["avgDistance"],results[(algo, direction, seed,"Ttest")]['avgDistance'][1],
        #                     groundTruth['effectiveDiameter'],
        #                     results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
        #                     results[(algo, direction, seed, "MeanEffectiveDiameter")][1],
        #                     results[(algo, direction, seed, "residuals")]["effectiveDiameter"],
        #                     results[(algo, direction, seed, "Ttest")]['effectiveDiameter'][1],
        #
        #                     groundTruth['lowerBoundDiameter'],
        #                     results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
        #                     results[(algo, direction, seed, "MeanLowerBoundDiameter")][1],
        #                     results[(algo, direction, seed, "residuals")]["lowerBoundDiameter"],
        #                     results[(algo, direction, seed, "Ttest")]['lowerBoundDiameter'][1],
        #
        #                     groundTruth['totalCouples'],
        #                     results[(algo, direction, seed, "MeanTotalCouples")][0],
        #                     results[(algo, direction, seed, "MeanTotalCouples")][1],
        #                     results[(algo, direction, seed, "residuals")]["totalCouples"],
        #                     results[(algo, direction, seed, "Ttest")]['totalCouples'][1]
        #
        #                 ])

        df = pd.DataFrame(elements,columns=head)
        df.round(rounding)
        df.to_csv(OutputPath+'.csv')

        if((LabelPath!= None) and (Ttest)):
            try:
                with open(LabelPath) as json_file:
                    newLabels = json.load(json_file)
            except IOError:
                print('Error! Can not open '+ LabelPath)
            #print(head)

            header =[]
            for elem in head:
                if(elem in newLabels.keys()):
                    header.append(elem)

            # The set operation does not preserve the original order.
            #header = list(set(head).intersection(set(newLabels.keys())))

            newHeads = []
            for name in header:
                newHeads.append(newLabels[name])


            relabeled = []
            for algo in algo_list:
                table = []
                for direction in direction_list:
                    for seed in seed_list:
                        table.append([
                            direction, seed,
                            groundTruth['avg_distance'],results[(algo, direction, seed,"MeanAvgDistance")][0],
                            str(results[(algo, direction, seed,"residuals")]["avg_distance"])+"% " +"("+str(results[(algo, direction, seed,"Ttest")]['avg_distance'])+")",
                            "+ - "+str(results[(algo, direction, seed, "confidence_Interval")]['avg_distance']),

                            groundTruth['effective_diameter'], results[(algo, direction, seed, "MeanEffectiveDiameter")][0],
                            str(results[(algo, direction, seed, "residuals")]["effective_diameter"]) + "% " +"(" + str(
                                results[(algo, direction, seed, "Ttest")]['effective_diameter']) + ")",
                            "+ - " + str(results[(algo, direction, seed, "confidence_Interval")]['effective_diameter']),

                            groundTruth['diameter'], results[(algo, direction, seed, "MeanLowerBoundDiameter")][0],
                            str(results[(algo, direction, seed, "residuals")]["diameter"]) + "% " +"(" + str(
                                results[(algo, direction, seed, "Ttest")]['diameter']) + ")",
                            "+ - " + str(results[(algo, direction, seed, "confidence_Interval")]['diameter']),

                            groundTruth['total_couples'], results[(algo, direction, seed, "MeanTotalCouples")][0],
                            str(results[(algo, direction, seed, "residuals")]["total_couples"])+"% " + "(" + str(
                                results[(algo, direction, seed, "Ttest")]['total_couples']) + ")",
                            "+ - " + str(results[(algo, direction, seed, "confidence_Interval")]['total_couples'])


                        ])
                relabeled.append(table)

            # # # one sided T TEST Between residual in-out
            # ttest = ro.r['t.test']
            # alternative = 'greater'
            # residual_test = []
            # if(in_direction and out_direction):
            #     #print(sample_residuals.keys())
            #     for algo in algo_list:
            #         avg_distance_in = []
            #         avg_distance_out = []
            #         effective_diameter_in = []
            #         effective_diameter_out = []
            #         diameter_in = []
            #         diameter_out = []
            #         couples_in = []
            #         couples_out = []
            #         for seed in seed_list:
            #             in_residual = sample_residuals[(algo, "in", seed,'avg_distance')]
            #             out_residual = sample_residuals[(algo, "out", seed,"avg_distance")]
            #             print(in_residual)
            #             avg_distance_in.append(in_residual)
            #             avg_distance_out.append(out_residual)
            #             xAvgD = ro.vectors.FloatVector(in_residual)
            #             yAvgD =  ro.vectors.FloatVector(out_residual)
            #             test_avg_distance = ttest(xAvgD, yAvgD, paired=False, alternative=alternative,
            #                                       conflevel=0.95)
            #
            #             in_residual = sample_residuals[(algo, "in", seed,"effective_diameter")]
            #             out_residual = sample_residuals[(algo, "out", seed,"effective_diameter")]
            #             effective_diameter_in.append(in_residual)
            #             effective_diameter_out.append(out_residual)
            #             xED =  ro.vectors.FloatVector(in_residual)
            #             yED = ro.vectors.FloatVector(out_residual)
            #             test_effective_diameter = ttest(xED, yED, paired=False, alternative=alternative,
            #                                             conflevel=0.95)
            #
            #
            #
            #             in_residual = sample_residuals[(algo, "in", seed,"diameter")]
            #             out_residual = sample_residuals[(algo, "out", seed,"diameter")]
            #             diameter_in.append(in_residual)
            #             diameter_out.append(out_residual)
            #             xD = ro.vectors.FloatVector(in_residual)
            #             yD = ro.vectors.FloatVector(out_residual)
            #
            #             test_diameter = ttest(xD, yD, paired=False, alternative=alternative,
            #                                   conflevel=0.95)
            #
            #
            #             in_residual = sample_residuals[(algo, "in", seed,"total_couples")]
            #             out_residual = sample_residuals[(algo, "out", seed,"total_couples")]
            #             couples_in.append(in_residual)
            #             couples_out.append(out_residual)
            #             xC = ro.vectors.FloatVector(in_residual)
            #             yC = ro.vectors.FloatVector(out_residual)
            #             test_couples = ttest(xC, yC, paired=False, alternative=alternative,
            #                                  conflevel=0.95)
            #
            #             avgd = test_avg_distance.rx2('p.value')[0]
            #             ed = test_effective_diameter.rx2('p.value')[0]
            #             di = test_diameter.rx2('p.value')[0]
            #             co =  test_couples.rx2('p.value')[0]
            #
            #             residual_test.append[algo,seed,
            #                 avgd, ed,di,co
            #                 ]
            #     heading = ['algorithm','seeds','pval_avg_distance_residual','pval_eff_diamenter_residual','pval_diameter_residual','pval_couples_residual']
            #     residualTestDf = pd.DataFrame(residual_test, columns=heading)
            #     #df.round(rounding)
            #     residualTestDf.to_csv(OutputPath +'_residualTest'+ '.csv')

                    # ttest = ro.r['t.test']
            # alternative = 'greater'
            # residual_test = []
            # if(in_direction and out_direction):
            #     for algo in algo_list:
            #         avg_distance_in = []
            #         avg_distance_out = []
            #         effective_diameter_in = []
            #         effective_diameter_out = []
            #         diameter_in = []
            #         diameter_out = []
            #         couples_in = []
            #         couples_out = []
            #         for seed in seed_list:
            #             # avg distance test
            #
            #             in_residual = results[(algo, "in", seed, "residuals")]["avg_distance"]
            #             out_residual = results[(algo, "out", seed, "residuals")]["avg_distance"]
            #             avg_distance_in.append(in_residual)
            #             avg_distance_out.append(out_residual)
            #
            #
            #
            #             in_residual = results[(algo, "in", seed, "residuals")]["effective_diameter"]
            #             out_residual = results[(algo, "out", seed, "residuals")]["effective_diameter"]
            #             effective_diameter_in.append(in_residual)
            #             effective_diameter_out.append(out_residual)
            #
            #
            #
            #             in_residual = results[(algo, "in", seed, "residuals")]["diameter"]
            #             out_residual = results[(algo, "out", seed, "residuals")]["diameter"]
            #             diameter_in.append(in_residual)
            #             diameter_out.append(out_residual)
            #
            #
            #             in_residual = results[(algo, "in", seed, "residuals")]["total_couples"]
            #             out_residual = results[(algo, "out", seed, "residuals")]["total_couples"]
            #             couples_in.append(in_residual)
            #             couples_out.append(out_residual)
            #
            #
            # xAvgD = ro.vectors.FloatVector(avg_distance_in)
            # yAvgD =  ro.vectors.FloatVector(avg_distance_out)
            # test_avg_distance = ttest(xAvgD, yAvgD, paired=False, alternative=alternative,
            #                           conflevel=0.95)
            # xED =  ro.vectors.FloatVector(effective_diameter_in)
            # yED = ro.vectors.FloatVector(effective_diameter_out)
            # test_effective_diameter = ttest(xED, yED, paired=False, alternative=alternative,
            #                                 conflevel=0.95)
            # xD = ro.vectors.FloatVector(diameter_in)
            # yD = ro.vectors.FloatVector(diameter_out)
            #
            # test_diameter = ttest(xD, yD, paired=False, alternative=alternative,
            #                       conflevel=0.95)
            # xC = ro.vectors.FloatVector(couples_in)
            # yC = ro.vectors.FloatVector(couples_out)
            # test_couples = ttest(xC, yC, paired=False, alternative=alternative,
            #                      conflevel=0.95)
            # residual_test.append[test_avg_distance.rx2('p.value')[0],test_effective_diameter.rx2('p.value')[0],test_diameter.rx2('p.value')[0],test_couples.rx2('p.value')[0]]
            # heading = ['pval_avg_distance_residual','pval_eff_diamenter_residual','pval_diameter_residual','pval_couples_residual']
            # residualTestDf = pd.DataFrame(residual_test, columns=heading)
            # #df.round(rounding)
            # residualTestDf.to_csv(OutputPath +'_residualTest'+ '.csv')

            i = 0

            for tab in relabeled:

                df_rel = pd.DataFrame(tab, columns=newHeads)
                df_rel.round(rounding)
                df_rel.to_csv(OutputPath + str(algo_list[i]) + '.csv')
                i+=1


    dict = {}
    for k,v in results.items():
        newkey= str()
        c = 0
        for elem in k:

            if(isinstance(elem,int)):

                newkey += str(elem)
            else:
                newkey += elem
            if(c<len(k)):
                newkey += ":"
            c+=1

        dict[newkey] = v



    with open(OutputPath+'.json', 'w') as outfile:
        json.dump(dict, outfile)

def main(argv):
   inputfile = ''
   outputfile = ''
   GroundTruthPath = None
   std = True
   Ttest = False
   df = False
   relabel = ''
   rounding = 5

   try:
      opts, args = getopt.getopt(argv,"hi:o:g:s:t:d:l:r:",["ifile=","ofile=","gfile=","std=","Ttest=","DF=","LAB=","ROUND="])
   except getopt.GetoptError:
        print("Error")
        sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-g","--gfile"):
          GroundTruthPath = arg
      elif opt in ("-s","--std"):
          if(arg in "-False"):
              std = False
          elif(arg in "-True"):
              std= True
      elif opt in ("-t","--Ttest"):

          if(arg in "-True" ):
              Ttest = True
          elif(arg in "-False"):
              Ttest = False
      elif opt in ("-d","--DF"):
          if (arg in "-True"):
              df = True
          elif (arg in "-False"):
              df = False
      elif opt in ("-l", "--LAB"):
          relabel = arg
      elif opt in ("-r","--ROUND"):
          rounding =int(arg)
   read_json(inputfile, outputfile, GroundTruthPath, std=std, Ttest=Ttest,dataframe=df,LabelPath=relabel,rounding = rounding)


if __name__ == "__main__":
   main(sys.argv[1:])

# Relabeling feature: DEMO version

# Input = "/Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/Parsati/worldSeries"
# Out = ""
# GroundTruthPath = "/Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/groundTruths/worldSeriesGT.json"
#
# read_json(Input,Out,GroundTruthPath,std = True,Ttest = True)
# Esempio di esecuzione
#  python readJson.py -i /Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/Parsati/worldSeriesRetweets -o /Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/worldSeriesRetweetsStats -g /Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/groundTruths/worldSeriesGT.json -s True -t True -d True -l /Users/antoniocruciani/Dropbox/EsperimentiDaAnalizzareFUB/TableRelabeling/relabel.json


