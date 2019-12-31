from bokeh.models.widgets import Div
from bokeh.models import Panel
from bokeh.layouts import column, row


def info_tab(citation_text):
    ##In this tab, all necessary info for videt is here - as well as the citations information for the chosen datasets
    ## after get_citation_boxfunction() is called

    static_info = Div(text=citation_text, sizing_mode="stretch_width")
    variable_info = Div(text="", sizing_mode="fixed")
    #This is a hack, but the communication between tabs doesn't work if I un-hack it.
    #TODO un-hack it
    layout = row(static_info, variable_info)

    tab = Panel(child=layout, title='Information')
    return tab
