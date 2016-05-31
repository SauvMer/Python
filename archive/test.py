import matplotlib

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as Tk

root = Tk.Tk()



fig = plt.figure(figsize=(12, 6))
map = Basemap(llcrnrlon=-4.476,llcrnrlat=48.417,urcrnrlon=-4.469,urcrnrlat=48.42, epsg=2154)
#map = Basemap(llcrnrlon=3.75,llcrnrlat=39.75,urcrnrlon=4.35,urcrnrlat=40.15, epsg=5520)

map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

map.drawcountries()
map.drawcoastlines(linewidth=.5)

x, y = map(-4.47, 48.418)
map.scatter(x,y,150,marker='o',color='r')
plt.show()


root.mainloop()

#plt.savefig('world.png',dpi=75)
