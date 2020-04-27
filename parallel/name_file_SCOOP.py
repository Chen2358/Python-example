#coding: utf-8

# 使用Scoop进行科学计算

#scoop是一个可扩展的Python并行计算库，https://scoop.readthedocs.io/en/0.7/install.html
#python –m scoop name_file_scoop.py
'''
import math
from random import random
from scoop import futures
from time import time


def evaluate_points_in_circle(attempts):
    points_fallen_in_unit_disk = 0
    for i in range (0,attempts) :
        x = random()
        y = random()
        radius = math.sqrt(x*x + y*y)
        if radius < 1 :
            points_fallen_in_unit_disk = points_fallen_in_unit_disk + 1
    return points_fallen_in_unit_disk

def pi_calculus_with_Montecarlo_Method(workers, attempts):
    print("number of workers %i - number of attempts %i" % (workers,attempts))
    bt = time()
    evaluate_task = futures.map(evaluate_points_in_circle, [attempts] * workers)
    taskresult= sum(evaluate_task)
    print ("%i points fallen in a unit disk after " %(taskresult/attempts))
    piValue = (4. * taskresult/ float(workers * attempts))
    computationalTime = time() - bt
    print("value of pi = " + str(piValue))
    print ("error percentage = " + str((((abs(piValue - math.pi)) * 100) / math.pi)))
    print("total time: " + str(computationalTime))

if __name__ == "__main__":
    for i in range (1,4):
        pi_calculus_with_Montecarlo_Method(i*1000, i*1000)
        print(" ")
'''


#通过SCOOP使用map函数
# python –m scoop name_file_scoop.py

import operator
import time
from  scoop import futures

def simulateWorkload(inputData):
    time.sleep(0.01)
    return sum(inputData)

def CompareMapReduce():
    mapScoopTime = time.time()
    res = futures.mapReduce(simulateWorkload,
                            operator.add,
                            list([a] * a for a in range(1000)),
                            )
    mapScoopTime = time.time() -  mapScoopTime
    print("futures.map in SCOOP executed in {0:.3f}s with result: {1}".format(mapScoopTime, res))

    mapPythonTime = time.time()
    res = sum(map(simulateWorkload, list([a] for a in range(1000))))
    mapPythonTime = time.time() - mapPythonTime
    print("map Python executed in: {0:.3f}s with result: {1}".format(mapPythonTime, res))

if __name__ == '__main__':
    CompareMapReduce()


























