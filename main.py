from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts import datasets
from scripts.plotting_tab import videt_tab
from scripts.info_tab import info_tab


# Read in list of implemented datasets
videt = datasets.data_collection()
videt.load("config/minimal_1")

# Create tabs and put them in the current document for display
tab2 = info_tab("")
tab1 = videt_tab(videt, tab2)
tabs = Tabs(tabs = [tab1, tab2])
curdoc().add_root(tabs)
curdoc().title = "videt  --  Hacking Ecology"


##TODO: write Readme with "how to run", first TODOs and list of datasets to implement