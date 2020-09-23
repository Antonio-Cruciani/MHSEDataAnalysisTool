# README

This is a Python script designed to analyze MinHash Signature Estimation Algorithm (MHSE).

## Table of Contents

- [Description](#Description)
- [MinHash Signature Estimation Algorithm](#MHSE)
- [Measurements from the Collision Table](#From-Collision-Table-to-Measurements)
- [How to analyze data](#Analysis)
- [License](#License)

## Description

This script allows you to analyze and fully reproduce our MHSE experiments.

## MHSE

MHSE is an algorithm to efficiently estimate the effective diameter and other distance metrics on very large graphs that are based on the neighborhood function such as the exact diameter, the (effective) radius or the average distance ([more details](https://www.semanticscholar.org/paper/Estimation-of-distance-based-metrics-for-very-large-Amati-Angelini/ca07e5fa517fc7567406ebc683dad35aa43758d4)) .
We currently have published two version of the algorithm: the original one (MHSE), and the space efficient one (SE-MHSE) that, produces the same outcomes of MHSE but with less space complexity.
SE-MHSE allows you to run this algorithm on machines with limited memory and also allows you to easily parallelize it using any map-reduce framework.
You can find our algorithm at the following [link](https://github.com/BigDataLaboratory/MHSE) . 

#### Algorithm output structure

The algorithm outputs the following json:
```json
{
  "collisionsTable": {"0" : [ 1, 1, 1, 1, 1, ..... }
  "minHashNodeIDs" : 
  "numSeeds" : 
  "numNodes" : 
  "numArcs" : 
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
If you execute the algorithm for more than one time, it will output a list of json.