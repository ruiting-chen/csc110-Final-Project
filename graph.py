# Some Plotly graphing code
import linear_regression

import plotly.graph_objects as go
import numpy as np

x = np.random.randint(-90, 90, 100)
y = np.random.randint(-180, 180, 100)
x = system.get_stations().location[]
# print(x)
# print(y)

fig = go.Figure(go.Scattergeo(lat=x, lon=y))
fig.update_layout(height=1000, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig.update_geos(showland=True, landcolor='Green',
                showocean=True, oceancolor='DarkBlue',
                showrivers=True, rivercolor='DarkBlue',
                showlakes=True, lakecolor='DarkBlue',
               showcountries=True, countrycolor='White')
fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
# fig.update_layout(height=1000)
fig.show()
