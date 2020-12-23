import rpy2.robjects as ro
import pandas as pd
import math as mt

def get_t_tests(inputFile,outputFile):

    data = pd.read_csv(inputFile)

    #directions = set(data['Message direction'].values)

    seeds = set(data['seeds'].values)
    results = []
    alt = "greater"
    ttest = ro.r['t.test']
    sd = ro.r['sd']
    qt = ro.r['qt']
    for seed in seeds:


        in_dir = data[(data['direction'] == 'in')&(data['seeds'] == seed)]
        out_dir = data[(data['direction'] == 'out')&(data['seeds'] == seed)]

        xAvgDistance = ro.vectors.FloatVector(in_dir['residualAvgDistance'])
        degrees = len(xAvgDistance) - 1
        yAvgDistance = ro.vectors.FloatVector(out_dir['residualAvgDistance'])

        resAvgDistance = ttest(xAvgDistance, yAvgDistance, paired=False, alternative=alt,
                               conflevel=0.95)



        xDiameter = ro.vectors.FloatVector(in_dir['residualLowerBoundDiameter'])
        yDiameter = ro.vectors.FloatVector(out_dir['residualLowerBoundDiameter'])


        resDiameter = ttest(xDiameter, yDiameter, paired=False, alternative=alt,
                               conflevel=0.95)




        xEffectiveDiameter = ro.vectors.FloatVector(in_dir['residualEffectiveDiameter'])
        yEffectiveDiameter = ro.vectors.FloatVector(out_dir['residualEffectiveDiameter'])


        resEffectiveDiameter = ttest(xEffectiveDiameter, yEffectiveDiameter, paired=False, alternative=alt,
                            conflevel=0.95)



        xCouples = ro.vectors.FloatVector(in_dir['residualTotalCouples'])
        yCouples = ro.vectors.FloatVector(out_dir['residualTotalCouples'])

        resCouples = ttest(xCouples, yCouples, paired=False, alternative=alt,
                                     conflevel=0.95)


        results.append(
            [
                seed,
                resAvgDistance.rx2('p.value')[0],
                resDiameter.rx2('p.value')[0],
                resEffectiveDiameter.rx2('p.value')[0],
                resCouples.rx2('p.value')[0],

            ]
        )
    header = ['seeds',
              'avg_distance',
              'diameter',
              'effective_diameter',
              'total_couples'
              ]
    df = pd.DataFrame(results,columns =header)
    df.to_csv(outputFile)

input =  '/home/antonio/Desktop/fub/with_iso/tomerge/combined_csv.csv'
output = '/home/antonio/Downloads/TESTresidual_with_iso.csv'
get_t_tests(input,output)