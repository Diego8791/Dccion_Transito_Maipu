#!/usr/bin/env python
'''
.............
.............
---------------------------
Autor: 
Version: 

Descripcion:
Programa creado...
'''

__author__ = "...."
__email__ = "...."
__version__ = "....."


import folium
import collections
from flask import request, jsonify


def location_map_individual(lat_long):     # lat_long contiene [latitud, longitud] para ubicar un accidente en consulta individual
    '''
    Se formará el mapa con número de accidente, latitud y longitud
    '''
    
    some_map = folium.Map(location=[lat_long[0], lat_long[1]], zoom_start=15, titles='localización de accidente')
    folium.Marker([lat_long[0], lat_long[1]], popop='<i>The Waterfront</i>').add_to(some_map)
    
    some_map.save('static/map_1.html')