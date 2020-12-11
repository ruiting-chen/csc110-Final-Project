"""
plot a map
"""
import plotly.express as px

gapminder = px.data.gapminder()
df = gapminder.query("year == 2007")
fig = px.scatter_geo(df, locations="iso_alpha",
                     color="continent",  # which column to use to set the color of markers
                     hover_name="country",  # column added to hover information
                     size="pop",  # size of markers
                     projection="natural earth")
fig.show()
