from bokeh.models.widgets import Div
from bokeh.models import Panel
from bokeh.layouts import column, row


def info_tab(citation_text):
    ##In this tab, all necessary info for videt is here - as well as the citations information for the chosen datasets
    ## after get_citation_boxfunction() is called

    static_info = Div(text="""This is videt (VIsualizing Dataset of Ecological Trends), which aims at supporting you by
       visualizing a variety of eco-related datasets in one place. This was created by Hacking Ecology. We are a
       open-source and open-data citizen science data science collective and we want to find out how to avert the sixth
       mass extinction by looking at datasets that are out there.""")

    #This is a hack, but the communication between tabs doesn't work if I un-hack it.
    #TODO un-hack it
    variable_info = Div(text = "")
    layout = row(static_info, variable_info)

    tab = Panel(child=layout, title='Information')
    return tab


