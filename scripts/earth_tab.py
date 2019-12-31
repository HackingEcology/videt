from bokeh.models.widgets import Div
from bokeh.models import Panel
from bokeh.layouts import row


def earth_tab():
    static_info = Div(text="""TODO""")

    variable_info = Div(text="")
    layout = row(static_info, variable_info)
    tab = Panel(child=layout, title='Map')
    return tab
