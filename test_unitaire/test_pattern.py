from pattern import *
import matplotlib.pyplot as plt
import numpy as np

if __name__=="__main__":

    plt.figure(1)

    #way = np.array(ratissage_sc(np.array([0,0]), 10, 1, 1.5, 1))
    way = np.array(balai(np.array([0,0]), np.array([10,10]), 1, 1))
    way = way.transpose()

    plt.plot(way[0], way[1])

    plt.show()
