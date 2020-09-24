# README

This is a Python script designed to analyze MinHash Signature Estimation Algorithm (MHSE).

## Table of Contents

- [Description](#Description)
- [MinHash Signature Estimation Algorithm](#MHSE)
    - [Description](#Short-Intro)
    - [Output structure](#Algorithm-output)
- [Measurements from the Collision Table](#From-Collision-Table-to-Measurements)
    - [Input structure](#Input)
- [How to analyze data](#Analysis)
    - [Input structure](#Input)
- [License](#License)

# Description

This script allows you to analyze and fully reproduce our MHSE experiments.
# MHSE
## Short-Intro

MHSE is an algorithm to efficiently estimate the effective diameter and other distance metrics on very large graphs that are based on the neighborhood function such as the exact diameter, the (effective) radius or the average distance ([more details](https://www.semanticscholar.org/paper/Estimation-of-distance-based-metrics-for-very-large-Amati-Angelini/ca07e5fa517fc7567406ebc683dad35aa43758d4)) .
Currently, we have published two version of the algorithm: the original one (MHSE), and the space efficient one (SE-MHSE) that, produces the same outcomes of MHSE but with less space complexity.
SE-MHSE allows you to run this algorithm on machines with limited memory and also to easily parallelize it using any map-reduce framework.
You can find our algorithm at the following [link](https://github.com/BigDataLaboratory/MHSE) . 

## Algorithm-output

The algorithm outputs the following JSON:
```text
{
  "collisionsTable" :
  "minHashNodeIDs"  :
  "numSeeds" :
  "numNodes"  :
  "numArcs"  :
  "seedsTime" :  
  "lastHops" :
  "time" :
  "lowerBoundDiameter" :  
  "totalCouples" :
  "totalCouplePercentage" : 
  "avgDistance" : 
  "effectiveDiameter" : 
  "algorithmName" : 
  "maxMemoryUsed" : 
  "seedsList" : 
  "threshold" : 
  "direction" : 
  "hopTable" : 
}
```
If you execute the algorithm more than once, it will output a list of JSON:
```text
[{
  "collisionsTable" :
  "minHashNodeIDs"  :
  .
  . 
  .
  "direction" : 
  "hopTable" : 
},{
  "collisionsTable" :
  "minHashNodeIDs"  :
  .
  . 
  .
  "direction" : 
  "hopTable" : 
},
  .
  . 
  .
]
```




# Analysis

##### USEFUL TIP
You can set the same output file for all your executions of the MHSE and\or SEMHSE obtaining a list of 
JSON of all the exectutions (or you can also create the list of JSON as a second step after all the experiments).
Given the JSON the script will automatically detect all the different parameters and group them all to calculate the statistics. 
 