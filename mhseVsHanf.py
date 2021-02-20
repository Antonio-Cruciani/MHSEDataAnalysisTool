import rpy2.robjects as ro
import pandas as pd
import math as mt

def get_t_tests(inputFileMhse,inputFileHyperAnf,outputFile):

    data = pd.read_csv(inputFileMhse)
    hdata = pd.read_csv(inputFileHyperAnf)
    #directions = set(data['Message direction'].values)


    results = []
    alt = "greater"
    ttest = ro.r['t.test']
    wilcoxon = ro.r['wilcox.test']
    # sd = ro.r['sd']
    # qt = ro.r['qt']


    in_dir = data[(data['direction'] == 'in')&(data['seeds'] == 256)]
    out_dir = data[(data['direction'] == 'out')&(data['seeds'] == 256)]

    xAvgDistanceIN = ro.vectors.FloatVector(in_dir['residualAvgDistance'])

    xAvgDistanceOUT = ro.vectors.FloatVector(out_dir['residualAvgDistance'])

    yAvgDistanceHAnf = ro.vectors.FloatVector(hdata['residualAvgDistance'])

    resAvgDistanceIN = ttest(xAvgDistanceIN, yAvgDistanceHAnf, paired=True, alternative=alt,
                           conflevel=0.95)
    resAvgDistanceINWilcoxon = wilcoxon(xAvgDistanceIN, yAvgDistanceHAnf, paired=True, alternative=alt,
                             conflevel=0.95)

    resAvgDistanceOUT = ttest(xAvgDistanceOUT, yAvgDistanceHAnf, paired=True, alternative=alt,
                             conflevel=0.95)

    resAvgDistanceOUTWilcoxon = wilcoxon(xAvgDistanceOUT, yAvgDistanceHAnf, paired=True, alternative=alt,
                              conflevel=0.95)



    xDiameterIN = ro.vectors.FloatVector(in_dir['residualLowerBoundDiameter'])
    xDiameterOUT = ro.vectors.FloatVector(out_dir['residualLowerBoundDiameter'])

    yDiameterHAnf =  ro.vectors.FloatVector(hdata['residualLowerBoundDiameter'])

    resDiameterIN = ttest(xDiameterIN, yDiameterHAnf, paired=True, alternative=alt,
                           conflevel=0.95)
    resDiameterINWilcoxon = wilcoxon(xDiameterIN, yDiameterHAnf, paired=True, alternative=alt,
                          conflevel=0.95)
    resDiameterOUT = ttest(xDiameterOUT, yDiameterHAnf, paired=True, alternative=alt,
                          conflevel=0.95)
    resDiameterOUTWilcoxon = wilcoxon(xDiameterOUT, yDiameterHAnf, paired=True, alternative=alt,
                           conflevel=0.95)




    xEffectiveDiameterIN = ro.vectors.FloatVector(in_dir['residualEffectiveDiameter'])
    xEffectiveDiameterOUT = ro.vectors.FloatVector(out_dir['residualEffectiveDiameter'])

    yEffectiveDiameterHAnf = ro.vectors.FloatVector(hdata['residualEffectiveDiameter'])


    resEffectiveDiameterIN = ttest(xEffectiveDiameterIN, yEffectiveDiameterHAnf, paired=True, alternative=alt,
                        conflevel=0.95)
    resEffectiveDiameterINWilcoxon = wilcoxon(xEffectiveDiameterIN, yEffectiveDiameterHAnf, paired=True, alternative=alt,
                                   conflevel=0.95)

    resEffectiveDiameterOUT = ttest(xEffectiveDiameterOUT, yEffectiveDiameterHAnf, paired=True, alternative=alt,
                                   conflevel=0.95)
    resEffectiveDiameterOUTWilcoxon = wilcoxon(xEffectiveDiameterOUT, yEffectiveDiameterHAnf, paired=True, alternative=alt,
                                    conflevel=0.95)



    xCouplesIN = ro.vectors.FloatVector(in_dir['residualTotalCouples'])
    xCouplesOUT = ro.vectors.FloatVector(out_dir['residualTotalCouples'])
    yCouplesHAnf = ro.vectors.FloatVector(hdata['residualTotalCouples'])

    resCouplesIN = ttest(xCouplesIN, yCouplesHAnf, paired=True, alternative=alt,
                                 conflevel=0.95)
    resCouplesINWilcoxon = wilcoxon(xCouplesIN, yCouplesHAnf, paired=True, alternative=alt,
                         conflevel=0.95)
    resCouplesOUT = ttest(xCouplesOUT, yCouplesHAnf, paired=True, alternative=alt,
                       conflevel=0.95)
    resCouplesOUTWilcoxon = wilcoxon(xCouplesOUT, yCouplesHAnf, paired=True, alternative=alt,
                          conflevel=0.95)

    results.append(
        [
            256,
            resAvgDistanceIN.rx2('p.value')[0],
            resAvgDistanceOUT.rx2('p.value')[0],
            resDiameterIN.rx2('p.value')[0],
            resDiameterOUT.rx2('p.value')[0],
            resEffectiveDiameterIN.rx2('p.value')[0],
            resEffectiveDiameterOUT.rx2('p.value')[0],
            resCouplesIN.rx2('p.value')[0],
            resCouplesOUT.rx2('p.value')[0],

            resAvgDistanceINWilcoxon.rx2('p.value')[0],
            resAvgDistanceOUTWilcoxon.rx2('p.value')[0],
            resDiameterINWilcoxon.rx2('p.value')[0],
            resDiameterOUTWilcoxon.rx2('p.value')[0],
            resEffectiveDiameterINWilcoxon.rx2('p.value')[0],
            resEffectiveDiameterOUTWilcoxon.rx2('p.value')[0],
            resCouplesINWilcoxon.rx2('p.value')[0],
            resCouplesOUTWilcoxon.rx2('p.value')[0],

        ]
    )
    header = ['seeds',
          'pval avg_distance Direction IN',
          'pval avg_distance Direction OUT',
          'pval diameter IN',
          'pval diameter OUT',
          'pval effective_diameter IN',
          'pval effective_diameter OUT',
          'pval total_couples IN',
          'pval total_couples OUT',

          'pval Wilcoxon avg_distance Direction IN',
          'pval Wilcoxon avg_distance Direction OUT',
          'pval Wilcoxon diameter IN',
          'pval Wilcoxon diameter OUT',
          'pval Wilcoxon effective_diameter IN',
          'pval Wilcoxon effective_diameter OUT',
          'pval Wilcoxon total_couples IN',
          'pval Wilcoxon total_couples OUT',

          ]
    df = pd.DataFrame(results,columns =header)
    df.to_csv(outputFile)

inputMHSE =  '/home/antonio/Downloads/mhse_with_iso.csv'
inputHyperAnf ="/home/antonio/Downloads/hb_with_iso.csv"
output = '/home/antonio/Downloads/TESTresidual_without_iso.csv'
get_t_tests(inputMHSE,inputHyperAnf,output)