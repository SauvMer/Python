# Structure
- archive
- sur_base
- sur_drone
- test_unitaire

# Dependencies
- Basemap : http://matplotlib.org/basemap/users/installing.html
- Dronekit : http://python.dronekit.io/develop/installation.html
- Dronekit-sitl : http://python.dronekit.io/develop/sitl_setup.html
- OpenCV : http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html#linux-installation

# Test
- test_basemap.py : test le chargement d'une carte grace au package Basemap
- test_clientserveur.py : test la communication client serveur
- test_pattern.py : test la generation de pattern
- test_pixy.py : test la detection avec Pixy CMU CAM 5 *(non utilisé)*
- test_vol.py : test l'envoie de commandes de vol avec dronekit
