import numpy as np

def balai(llcorner, trcorner, l,ori):
    waypoints=[llcorner]
    i=0

    while waypoints[-1][0] < trcorner[0]:
        x= waypoints[-1][0]
        if i%2 != 0:
           x = x + l

        if int(i/2)%2 == 0:
            waypoints.append(np.array([x,trcorner[1]]))
        else:
            waypoints.append(np.array([x,llcorner[1]]))
        i=i+1

    return np.array(waypoints).dot(np.array([[np.cos(ori), np.sin(ori)],[-np.sin(ori), np.cos(ori)]]))


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