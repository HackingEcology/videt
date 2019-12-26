# pandas and numpy for data manipulation

import numpy as np

from bokeh.plotting import figure
from bokeh.models import Panel, HoverTool, Legend
from bokeh.models.widgets import (CheckboxGroup, Div, Button)
from bokeh.layouts import column, row, WidgetBox


def videt_tab(dataset_collection, infos_tab):

    def style(p):
        ## Defines a plotting style
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p


    def update_plot_after_checkbox(attr, old, new):
        #This function updates the plot according to the active checkboxes; therefore, here, all the relevant info is
        #read from the dataset object
        colors = ["black", "red", "green", "blue", "yellow", "pink"] #TODO automatically generate a fitting number of colors

        #re-initialize the plot by removing all renderers
        tab.child.children[1] = figure(plot_width=600, plot_height=600, title="", x_axis_type="datetime")
        plot_object = tab.child.children[1]
        plot_object = style(plot_object)
        plot_object.xaxis.axis_label = "Time"
        plot_object.yaxis.axis_label = "Value" ##TODO this isn't perfect yet

        #Initialize p_dict to store all necessary information for the legend
        p_dict = dict()

        for i, this_dataset in enumerate(dataset_collection.datasets):
            ##go through the carrier selection and plot the activated datasets
            if i in carrier_selection.active:
                if not this_dataset.is_loaded:
                    this_dataset.load_data()

                for y_col, y_label, c in zip(this_dataset.y_columns, this_dataset.y_labels, colors):
                    p_dict[y_label] = \
                        plot_object.line(x='x', y=y_col, source=this_dataset.data, color=c, line_width=2)
                    #plot_object.add_tools(HoverTool(
                    #    renderers=[p_dict[y_label]],
                    #    tooltips=[('datetime', '@index{%Y-%m-%d %H:%M:%S}'), (y_label, f'@{y_label}')],
                    #    formatters={'index': 'datetime'}
                    #))
        ##TODO make the Legend work!
        legend = Legend(items=[(x, [p_dict[x]]) for x in p_dict])
        plot_object.add_layout(legend, 'right')


    def get_citation_boxfunction():
        ##This function is called by pressing citation_button and prints the relevant info to cite to the info_tab
        ##TODO make sure that the user knows where to look for the output
        citation_header = "Citation for chosen datasets:\n\r"
        citation_lines = ""
        for i, this_dataset in enumerate(dataset_collection.datasets):
            if i in carrier_selection.active:
                citation_lines += "<p>" + str(this_dataset) + ": " + this_dataset.get_citation() + " </p>"

        if citation_lines != "":
            citation_lines = citation_header + citation_lines
        else:
            citation_lines = "No datasets chosen."

        infos_tab.child.children[1] = Div(text = citation_lines)


    ##Initialize empty plot
    p = figure(plot_width=600, plot_height=600, title="", x_axis_type="datetime")
    ##TODO add datime x axis by default
    ##TODO do something so that the "Plot has no renderers" warning doesnt show up -- maybe create a fancy default plot

    #Add a checkbox for each dataset in the dataset collection
    carrier_selection = CheckboxGroup(labels = [str(dataset) for dataset in dataset_collection.datasets],
                                      active = [])
    ##Datasets are only loaded when the checkbox is checked for the first time, and immediately plotted
    carrier_selection.on_change('active', update_plot_after_checkbox)

    # Put all control elements in a single layout
    p = style(p)
    p.xaxis.axis_label = "Time"
    p.yaxis.axis_label = "Value"
    dataset_choice_checkboxes = WidgetBox(carrier_selection)
    citation_button = Button(label="Get citation for chosen datasets", button_type="success")
    citation_button.on_click(get_citation_boxfunction)
    layout = row(column(dataset_choice_checkboxes, citation_button), p)

    # Create a tab with the layout
    tab = Panel(child=layout, title = 'Videt')

    ##TODO add a button to download the shown data

    return tab
