import numpy as np
import matplotlib.pyplot as plt

def ratissage_sc(centre, distance, l, L, ori):
    waypoints=[centre]
    i = 0
    n = 1
    while max(n*l,n*L) < distance:
        if i%2 == 0:
            if n%2 == 0:
                waypoints.append(waypoints[-1]+np.array([-n*L,0]))
            else:
                waypoints.append(waypoints[-1]+np.array([n*L,0]))
        else:
            if n%2 == 0:
                waypoints.append(waypoints[-1]+np.array([0,-n*l]))
            else:
                waypoints.append(waypoints[-1]+np.array([0,n*l]))
        i=i+1
        if i%2 == 0:
            n=n+1

    return np.array(waypoints).dot(np.array([[np.cos(ori), np.sin(ori)],[-np.sin(ori), np.cos(ori)]]))

if __name__=="__main__":

    plt.figure(1)

    way = np.array(ratissage_sc(np.array([0,0]), 10,1,1.5, 1))
    way = way.transpose()

    plt.plot(way[0], way[1])

    plt.show()