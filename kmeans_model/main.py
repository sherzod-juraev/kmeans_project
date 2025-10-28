from .model import KMeans
from random import uniform
from numpy import zeros
from datetime import datetime

kmeans = KMeans(3)
if __name__ == '__main__':
    array = zeros([2000, 2], dtype=float)
    for i in range(2000):
        array[i][0] = uniform(0, 100)
        array[i][1] = uniform(0, 100)
        array[i][0] = round(array[i][0], 2)
        array[i][1] = round(array[i][1], 2)
    start = datetime.now()
    kmeans.fit(array)
    end_time =  datetime.now()
    print('time=', end_time - start)