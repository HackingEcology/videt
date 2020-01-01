# pandas and numpy for data manipulation

import numpy as np

from bokeh.plotting import figure
from bokeh.models import Panel, HoverTool, Legend
from bokeh.models.widgets import (CheckboxGroup, Div, Button)
from bokeh.layouts import column, row, WidgetBox
from bokeh.palettes import d3

def videt_tab(dataset_collection, infos_tab, citation_header):

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

    def get_iter_of_colors(collection_of_datasets, checkboxes):
        ##This function is counting the number of active (sub-) datasets and then assign a color list of the
        # correct size
        #TODO make this "stable" in any way, so that colors remain the same even if things are added or removed;
        dataset_counter = 0
        for i, this_dataset in enumerate(collection_of_datasets.datasets):
            if i in checkboxes.active:
                for y_label in this_dataset.y_labels:
                    dataset_counter += 1
        if dataset_counter == 0:
            colors = []
        elif dataset_counter == 1:
            colors = ["black"]
        else:
            colors = d3['Category20'][dataset_counter]
        return iter(colors)

    def update_plot_after_checkbox(attr, old, new):
        #This function updates the plot according to the active checkboxes; therefore, here, all the relevant info is
        #read from the dataset object

        #re-initialize the plot by removing all renderers
        tab.child.children[1] = figure(title="", x_axis_type="datetime")
        plot_object = tab.child.children[1]
        plot_object = style(plot_object)
        plot_object.xaxis.axis_label = "Time"
        plot_object.yaxis.axis_label = "Value" ##TODO this isn't perfect yet

        #Initialize p_dict to store all necessary information for the legend
        p_dict = dict()

        ##Counting the number of active (sub-) datasets and then assign a color list of the correct size
        colors = get_iter_of_colors(dataset_collection, carrier_selection)

        for i, this_dataset in enumerate(dataset_collection.datasets):
            ##Goes through the carrier selection chechboxes and plot the activated datasets
            if i in carrier_selection.active:
                if not this_dataset.is_loaded:
                    this_dataset.load_data()

                for y_col, y_label in zip(this_dataset.y_columns, this_dataset.y_labels):
                    p_dict[y_label] = \
                        plot_object.line(x='x', y=y_col, source=this_dataset.data, color=next(colors), line_width=2)
                    #plot_object.add_tools(HoverTool(
                    #    renderers=[p_dict[y_label]],
                    #    tooltips=[('datetime', '@index{%Y-%m-%d %H:%M:%S}'), (y_label, f'@{y_label}')],
                    #    formatters={'index': 'datetime'}
                    #))

        for x in p_dict:
            print(x)
            print(p_dict[x])
            print()

        legend = Legend(items=[(x, [p_dict[x]]) for x in p_dict])
        plot_object.add_layout(legend)

        # pass on citation information to the information tab
        update_citation()

    def update_citation():
        citation_lines = ""

        for i, this_dataset in enumerate(dataset_collection.datasets):
            ##Goes through the carrier selection chechboxes and gets the relevant citation lines
            if i in carrier_selection.active:
                citation_lines += "<p>" + str(this_dataset) + ": " + this_dataset.get_citation() + " </p>"

        # pass on citation information to the information tab
        if citation_lines != "":
            citation_lines = citation_header + citation_lines
        else:
            citation_lines = citation_header

        infos_tab.child.children[0] = Div(text=citation_lines, sizing_mode="stretch_width")

    def gather_and_save_data_on_click():
        None
        #TODO write this

    ##Initialize empty plot
    #p = figure(plot_width=600, plot_height=600, title="", x_axis_type="datetime")
    p = figure(title="", x_axis_type="datetime")
    p = style(p)
    p.xaxis.axis_label = "Time"
    p.yaxis.axis_label = "Value"

    ##TODO add datime x axis by default
    ##TODO do something so that the "Plot has no renderers" warning doesnt show up -- maybe create a fancy default plot

    #TODO think about how to make datasets chooseable better. E.G. only make those datasets chooseable at first that
    # do not need geolocation; and only make those chooseable after the user has chosen a geolocation in the geo tab.

    #Add a checkbox for each dataset in the dataset collection
    carrier_selection = CheckboxGroup(labels = [str(dataset) for dataset in dataset_collection.datasets],
                                      active = [])
    ##Datasets are only loaded when the checkbox is checked for the first time, and immediately plotted
    carrier_selection.on_change('active', update_plot_after_checkbox)

    # Put all control elements in a single layout
    dataset_choice_checkboxes = WidgetBox(carrier_selection)
    ##TODO add the possibility to download the shown data on click
    downloader_button = Button(label="Download Data as CSV", button_type="success")
    downloader_button.on_click(gather_and_save_data_on_click)
    layout = row(column(dataset_choice_checkboxes, downloader_button), p)

    # Create a tab with the layout
    tab = Panel(child=layout, title = 'Visualize')

    return tab
