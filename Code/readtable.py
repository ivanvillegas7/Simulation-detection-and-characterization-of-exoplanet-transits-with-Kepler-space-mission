# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:31:04 2023

@author: usuariouc
"""

import pandas as pd

url = 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative'

# Leer la tabla desde la URL
dfs = pd.read_html(url)

# Acceder al primer DataFrame de la lista
df = dfs[0]

# Filtrar solo los planetas confirmados y con una masa menor a 5 veces la masa de Júpiter
df_filtered = df[(df['pl_discmethod'] == 'Radial Velocity') & (df['pl_bmassj'] < 5)]

# Mostrar solo algunas columnas
columns = ['pl_name', 'pl_discmethod', 'pl_bmassj']
print(df_filtered[columns])
