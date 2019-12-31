from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts import datasets
from scripts.plotting_tab import videt_tab
from scripts.info_tab import info_tab
from scripts.earth_tab import earth_tab

# Read in list of implemented datasets
videt = datasets.data_collection()
videt.load("config/minimal_1")

info_default_string = """<p style="text-align: center;"><strong>This is <br /></strong></p>
<h1 style="text-align: center;"><strong>videt</strong></h1>
<p style="text-align: center;">(<span style="text-decoration: underline;">VI</span>sualizing
<span style="text-decoration: underline;">D</span>ataset of
<span style="text-decoration: underline;">E</span>cological
<span style="text-decoration: underline;">T</span>rends)</p>
<p style="text-align: center;">a tool by  <a href="https://hackingecology.eu/">Hacking Ecology</a>.</p>
<p>videt aims at supporting you by visualizing a variety of eco-related time series datasets in one place. If you want
to display geographically defined datasets, please first set a location in the "Map" tab, then proceed to the
"Visualize" tab; if you want to look only at global datasets, you can proceed directly to the "Visualize" tab.
Citation lines for chosen datasets will show up here after chosing datasets:</p>"""


# Create tabs and put them in the current document for display
tab_earth = earth_tab()
tab_info = info_tab(info_default_string)
tab_data = videt_tab(videt, tab_info, info_default_string)
tabs = Tabs(tabs = [tab_info, tab_earth, tab_data])
curdoc().add_root(tabs)
curdoc().title = "videt  --  Hacking Ecology"