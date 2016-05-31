from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=-4.476,llcrnrlat=48.417, urcrnrlon=-4.469, urcrnrlat=48.42, epsg=2154)

map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000, verbose=True)

plt.show()
